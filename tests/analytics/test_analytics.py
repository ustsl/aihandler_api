from tests.conftest import HEADERS, client


def test_analytics_requires_service_token():
    response = client.get("v1/analytics/queries")
    assert response.status_code == 401


def test_analytics_queries_returns_expected_shape(user_data_with_money, prompt_data):
    create_response = client.post(
        f'v1/queries/{user_data_with_money["telegram_id"]}',
        json={"prompt_id": prompt_data["id"], "query": "analytics-shape"},
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )
    assert create_response.status_code == 200

    response = client.get("v1/analytics/queries", headers=HEADERS)
    assert response.status_code == 200
    payload = response.json()
    assert "result" in payload
    assert "total" in payload
    assert isinstance(payload["result"], list)
