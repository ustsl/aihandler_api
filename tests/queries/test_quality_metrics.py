from src.api.queries.modules.quality_metrics import build_query_quality_metrics
from src.api.queries.schemas import UserQueryResult


def test_quality_metrics_for_text_response():
    metrics = build_query_quality_metrics(
        query="How can I optimize SQL query performance?",
        result="Use indexes, analyze execution plans, and avoid selecting unused columns.",
    )

    assert metrics["response_type"] == "text"
    assert metrics["word_count"] > 0
    assert metrics["sentence_count"] > 0
    assert 0 <= metrics["overall_score"] <= 1
    assert metrics["cached"] is False


def test_quality_metrics_for_url_response():
    metrics = build_query_quality_metrics(
        query="Generate an image of a red fox",
        result="https://cdn.example.com/generated/red-fox.png",
        cached=True,
    )

    assert metrics["response_type"] == "url"
    assert metrics["word_count"] >= 1
    assert metrics["sentence_count"] == 0
    assert metrics["cached"] is True


def test_user_query_result_schema_accepts_quality_metrics():
    payload = {
        "result": "Hello",
        "cost": 0.01,
        "quality_metrics": build_query_quality_metrics(
            query="Say hello",
            result="Hello",
        ),
    }

    parsed = UserQueryResult(**payload)
    assert parsed.result == "Hello"
    assert parsed.quality_metrics.response_type == "text"
