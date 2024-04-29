from tests.conftest import client

from tests.prompts.fixtures import *
import pytest
from tests.conftest import client


def test_query_story():
    headers = HEADERS
    query = f"v1/queries/"
    response = client.get(
        query,
        headers=headers,
    )
    assert len(response.json().get("result")) > 0
