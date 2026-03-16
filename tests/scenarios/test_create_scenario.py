from tests.conftest import HEADERS, client


def test_success_create_scenario(
    scenario_prompt_data, special_prompts_list, user_data_with_prompt
):
    telegram_id = user_data_with_prompt["telegram_id"]
    headers = {"Authorization": user_data_with_prompt["token"]["token"]}

    assert scenario_prompt_data["title"] == "Scenario1"

    update_scenario_body = {
        "title": "Scenario1",
        "description": "",
        "prompts": [
            {
                "prompt_id": special_prompts_list[0]["id"],
                "order": 2,
                "independent": False,
            },
            {
                "prompt_id": special_prompts_list[1]["id"],
                "order": 1,
                "independent": True,
            },
        ],
    }

    scenario_update_response = client.put(
        f'v1/scenarios/{telegram_id}/{scenario_prompt_data["id"]}',
        json=update_scenario_body,
        headers=headers,
    )
    assert scenario_update_response.status_code == 200
    scenario_with_relations = scenario_update_response.json()

    top_up_response = client.put(
        f"v1/users/{telegram_id}/balance",
        json={"balance": 10},
        headers=HEADERS,
    )
    assert top_up_response.status_code == 200

    scenario_query_response = client.post(
        f"v1/queries/{telegram_id}/scenario",
        json={"scenario_id": scenario_with_relations["uuid"], "query": "2"},
        headers=headers,
    )

    assert scenario_query_response.status_code == 200
    scenario_query = scenario_query_response.json()
    assert len(scenario_query) == 2
    assert scenario_query[1]["result"] == "8"
