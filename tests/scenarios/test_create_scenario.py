from tests.conftest import client
from tests.scenarios.fixtures import *


async def test_success_create_scenario(
    scenario_prompt_data, special_prompts_list, user_data_with_prompt
):

    user_data = user_data_with_prompt

    telegram_id = user_data.get("telegram_id")

    token = user_data.get("token").get("token")
    headers = {"Authorization": token}

    scenario_data = scenario_prompt_data
    assert scenario_data.get("title") == "Scenario1"

    prompts = special_prompts_list

    update_scenario_body = {
        "title": "Scenario1",
        "description": "",
        "prompts": [
            {
                "prompt_id": prompts[0].get("id"),
                "order": 2,
                "independent": False,
            },
            {
                "prompt_id": prompts[1].get("id"),
                "order": 1,
                "independent": True,
            },
        ],
    }

    scenario_with_relations = client.put(
        f"v1/scenarios/{telegram_id}/{scenario_data.get("id")}",
        json=update_scenario_body,
        headers=headers,
    )

    scenario_with_relations = scenario_with_relations.json()

    post_query_body = {"scenario_id": scenario_with_relations.get("uuid"), "query": "2"}

    balance = client.put(
        f"v1/users/{telegram_id}/balance",
        json={"balance": 10},
        headers=HEADERS,
    )

    print(balance.json())

    scenario_query = client.post(
        f"v1/queries/{telegram_id}/scenario",
        json=post_query_body,
        headers=headers,
    )

    scenario_query = scenario_query.json()
    assert len(scenario_query) == 2
    assert scenario_query[1].get("result") == "8"
