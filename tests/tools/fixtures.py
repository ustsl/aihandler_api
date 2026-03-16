import uuid

import pytest

from tests.conftest import client


def _tool_payload(name: str, url: str = "https://api.example.com/tool") -> dict:
    return {
        "name": name,
        "description": "Test tool",
        "transport": "http_json",
        "method": "POST",
        "url": url,
        "input_schema": {
            "type": "object",
            "required": ["value"],
            "properties": {"value": {"type": "number"}},
        },
        "headers_template": {},
        "query_template": {},
        "body_template": {},
        "auth_type": "none",
        "timeout_sec": 10,
        "max_response_bytes": 262144,
        "is_active": True,
    }


@pytest.fixture()
def create_tool_for_user():
    def _factory(user_data: dict, *, name: str | None = None, url: str | None = None):
        tool_name = name or f"tool_{uuid.uuid4().hex[:10]}"
        payload = _tool_payload(name=tool_name, url=url or "https://api.example.com/tool")
        response = client.post(
            f'v1/tools/{user_data["telegram_id"]}',
            json=payload,
            headers={"Authorization": user_data["token"]["token"]},
        )
        assert response.status_code == 200
        return response.json()

    return _factory
