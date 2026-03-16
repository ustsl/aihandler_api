from tests.conftest import client


def _create_scenario(user_data: dict, title: str = "Scenario extra") -> dict:
    response = client.post(
        f'v1/scenarios/{user_data["telegram_id"]}',
        json={"title": title, "description": "desc"},
        headers={"Authorization": user_data["token"]["token"]},
    )
    assert response.status_code == 200
    return response.json()


def test_create_scenario_invalid_title_returns_422(user_data_with_prompt):
    response = client.post(
        f'v1/scenarios/{user_data_with_prompt["telegram_id"]}',
        json={"title": "Bad@Title", "description": "desc"},
        headers={"Authorization": user_data_with_prompt["token"]["token"]},
    )
    assert response.status_code == 422


def test_get_scenario_detail_not_found_returns_404(user_data_with_prompt):
    response = client.get(
        f'v1/scenarios/{user_data_with_prompt["telegram_id"]}/b35273d1-e135-43e3-aae5-c9997276479d',
        headers={"Authorization": user_data_with_prompt["token"]["token"]},
    )
    assert response.status_code == 404


def test_delete_scenario_then_detail_returns_404(user_data_with_prompt):
    scenario = _create_scenario(user_data_with_prompt, title="Scenario delete check")

    delete_response = client.delete(
        f'v1/scenarios/{user_data_with_prompt["telegram_id"]}/{scenario["id"]}',
        headers={"Authorization": user_data_with_prompt["token"]["token"]},
    )
    assert delete_response.status_code == 200

    detail_response = client.get(
        f'v1/scenarios/{user_data_with_prompt["telegram_id"]}/{scenario["id"]}',
        headers={"Authorization": user_data_with_prompt["token"]["token"]},
    )
    assert detail_response.status_code == 404


def test_start_scenario_not_found_returns_404(user_data_with_prompt):
    response = client.post(
        f'v1/queries/{user_data_with_prompt["telegram_id"]}/scenario',
        json={
            "scenario_id": "b35273d1-e135-43e3-aae5-c9997276479d",
            "query": "hello",
        },
        headers={"Authorization": user_data_with_prompt["token"]["token"]},
    )
    assert response.status_code == 404
