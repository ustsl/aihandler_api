from tests.conftest import client
from tests.prompts.fixtures import *
from tests.users.fixtures import *


def get_user(user_id):
    user_data = client.get(
        f"v1/users/{user_id}",
        headers=HEADERS,
    )
    return user_data.json()


def test_user_set_language(user_data_with_money):

    user_data = user_data_with_money
    tg_id = user_data.get("telegram_id")
    assert user_data.get("settings").get("language") == None

    api_link = f"v1/users/{tg_id}/settings"

    client.put(
        api_link,
        json={"language": "eng"},
        headers=HEADERS,
    )

    user_data = get_user(tg_id)

    assert user_data.get("settings").get("language") == None

    client.put(
        api_link,
        json={"language": "en"},
        headers=HEADERS,
    )

    user_data = get_user(tg_id)

    assert user_data.get("settings").get("language") == "en"
