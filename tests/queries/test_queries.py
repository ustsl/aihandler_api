from tests.conftest import HEADERS, client


def test_gpt_query_uses_cache_and_deducts_balance_once(user_data_with_money, prompt_data):
    headers = {"Authorization": user_data_with_money["token"]["token"]}
    query_url = f'v1/queries/{user_data_with_money["telegram_id"]}'

    first_response = client.post(
        query_url,
        json={
            "prompt_id": prompt_data["id"],
            "query": "merhaba",
        },
        headers=headers,
    )
    second_response = client.post(
        query_url,
        json={
            "prompt_id": prompt_data["id"],
            "query": "merhaba",
        },
        headers=headers,
    )

    first_data = first_response.json()
    second_data = second_response.json()

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert first_data["result"].lower() == "hello"
    assert second_data["result"].lower() == "hello"
    assert first_data["cost"] > 0
    assert second_data["cost"] == 0
    assert second_data["quality_metrics"]["cached"] is True

    user_response = client.get(
        f'v1/users/{user_data_with_money["telegram_id"]}',
        headers=HEADERS,
    )
    balance = float(user_response.json()["accounts"]["balance"])
    assert 0.49 < balance < 0.5


def test_gpt_query_no_balance(prompt_data, user_data_with_prompt):
    headers = {"Authorization": user_data_with_prompt["token"]["token"]}
    query_url = f'v1/queries/{user_data_with_prompt["telegram_id"]}'

    response = client.post(
        query_url,
        json={
            "prompt_id": prompt_data["id"],
            "query": "merhaba merhaba",
        },
        headers=headers,
    )

    assert response.status_code == 403


def _create_prompt_with_model(user_data: dict, model: str) -> dict:
    response = client.post(
        f'v1/prompts/{user_data["telegram_id"]}',
        json={
            "title": f"Prompt {model.replace('-', ' ')}",
            "description": "Test descr",
            "prompt": "Medical transcription context",
            "model": model,
            "is_open": True,
            "context_story_window": 0,
            "tuning": {},
        },
        headers={"Authorization": user_data["token"]["token"]},
    )
    assert response.status_code == 200
    return response.json()


def test_text_query_rejects_audio_prompt(user_data_with_money):
    prompt = _create_prompt_with_model(user_data_with_money, "gpt-4o-mini-transcribe")

    response = client.post(
        f'v1/queries/{user_data_with_money["telegram_id"]}',
        json={
            "prompt_id": prompt["id"],
            "query": "transcribe this",
        },
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )

    assert response.status_code == 400
    assert "multipart file upload" in response.json()["detail"]


def test_file_query_rejects_text_prompt(prompt_data, user_data_with_money):
    response = client.post(
        f'v1/queries/{user_data_with_money["telegram_id"]}/file',
        data={"prompt_id": prompt_data["id"], "query": "context"},
        files={"file": ("voice.mp3", b"audio-bytes", "audio/mpeg")},
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )

    assert response.status_code == 400
    assert "only audio transcription prompts" in response.json()["detail"]


def test_file_query_requires_multipart_file(user_data_with_money):
    prompt = _create_prompt_with_model(user_data_with_money, "gpt-4o-mini-transcribe")

    response = client.post(
        f'v1/queries/{user_data_with_money["telegram_id"]}/file',
        json={
            "prompt_id": prompt["id"],
            "query": "context",
        },
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )

    assert response.status_code == 400
    assert "Audio file is required" in response.json()["detail"]


def test_file_query_sends_audio_to_gpt_handler(user_data_with_money, gpt_call_log):
    prompt = _create_prompt_with_model(user_data_with_money, "gpt-4o-mini-transcribe")

    response = client.post(
        f'v1/queries/{user_data_with_money["telegram_id"]}/file',
        data={"prompt_id": prompt["id"], "query": "terms: Cardiology"},
        files={"file": ("voice.wav", b"audio-bytes", "audio/wav")},
        headers={"Authorization": user_data_with_money["token"]["token"]},
    )

    assert response.status_code == 200
    assert gpt_call_log[-1]["model"] == "gpt-4o-mini-transcribe"
    assert gpt_call_log[-1]["message"] == "terms: Cardiology"
    assert gpt_call_log[-1]["file_bytes"] == b"audio-bytes"
    assert gpt_call_log[-1]["filename"] == "voice.wav"
    assert gpt_call_log[-1]["content_type"] == "audio/wav"
