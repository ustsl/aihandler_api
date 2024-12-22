from tests.conftest import client
from tests.prompts.fixtures import *


def test_query_story():
    headers = HEADERS
    query = f"v1/analytics/queries/"
    response = client.get(
        query,
        headers=headers,
    )
    assert len(response.json().get("result")) > 0
