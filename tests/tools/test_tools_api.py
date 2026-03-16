from tests.conftest import client


def test_create_list_get_tool(user_data_with_money):
    create_response = client.post(
        f'v1/tools/{user_data_with_money["telegram_id"]}',
        json={
            "name": "sum_tool_main",
            "description": "Sum tool",
            "transport": "http_json",
            "method": "POST",
            "url": "https://api.example.com/sum",
            "input_schema": {"type": "object", "required": ["value"]},
            "headers_template": {},
            "query_template": {},
            "body_template": {},
            "auth_type": "none",
            "timeout_sec": 10,
            "max_response_bytes": 262144,
            "is_active": True,
        },
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )
    assert create_response.status_code == 200
    tool = create_response.json()

    list_response = client.get(
        f'v1/tools/{user_data_with_money["telegram_id"]}',
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )
    assert list_response.status_code == 200
    assert any(item["uuid"] == tool["uuid"] for item in list_response.json()["result"])

    get_response = client.get(
        f'v1/tools/{user_data_with_money["telegram_id"]}/{tool["uuid"]}',
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "sum_tool_main"


def test_update_and_delete_tool_owner(user_data_with_money, create_tool_for_user):
    tool = create_tool_for_user(user_data_with_money, name="owner_tool_update")

    update_response = client.put(
        f'v1/tools/{user_data_with_money["telegram_id"]}/{tool["uuid"]}',
        json={"description": "Updated description", "timeout_sec": 20},
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )
    assert update_response.status_code == 200
    assert update_response.json()["description"] == "Updated description"
    assert update_response.json()["timeout_sec"] == 20

    delete_response = client.delete(
        f'v1/tools/{user_data_with_money["telegram_id"]}/{tool["uuid"]}',
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )
    assert delete_response.status_code == 200

    get_after_delete_response = client.get(
        f'v1/tools/{user_data_with_money["telegram_id"]}/{tool["uuid"]}',
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )
    assert get_after_delete_response.status_code == 404


def test_update_foreign_tool_forbidden(
    user_data_with_money, user_data_with_prompt, create_tool_for_user
):
    tool = create_tool_for_user(user_data_with_money, name="foreign_tool_forbidden")

    response = client.put(
        f'v1/tools/{user_data_with_prompt["telegram_id"]}/{tool["uuid"]}',
        json={"description": "should fail"},
        headers={"Authorization": user_data_with_prompt["token"]["token"]},
    )
    assert response.status_code == 404


def test_create_tool_invalid_name_returns_422(user_data_with_money):
    response = client.post(
        f'v1/tools/{user_data_with_money["telegram_id"]}',
        json={
            "name": "bad-tool-name!",
            "description": "Bad",
            "transport": "http_json",
            "method": "POST",
            "url": "https://api.example.com/x",
            "input_schema": {"type": "object"},
            "auth_type": "none",
        },
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )
    assert response.status_code == 422
