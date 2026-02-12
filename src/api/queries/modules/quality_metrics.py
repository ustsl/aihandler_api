import re
from urllib.parse import urlparse


WORD_RE = re.compile(r"[0-9A-Za-zА-Яа-яЁё]+")


def _clamp(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    return max(min_value, min(max_value, value))


def _tokenize(text: str) -> list[str]:
    return [token.lower() for token in WORD_RE.findall(text or "")]


def _is_url(value: str) -> bool:
    if not value:
        return False
    parsed = urlparse(value.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _count_sentences(text: str) -> int:
    parts = [part.strip() for part in re.split(r"[.!?]+", text or "") if part.strip()]
    return len(parts)


def _round_metric(value: float) -> float:
    return round(float(value), 4)


def build_query_quality_metrics(query: str, result: str, cached: bool = False) -> dict:
    query_text = query or ""
    result_text = (result or "").strip()

    response_type = "url" if _is_url(result_text) else "text"
    words = _tokenize(result_text)
    query_words = set(_tokenize(query_text))
    result_words = set(words)

    char_count = len(result_text)
    word_count = len(words)
    sentence_count = _count_sentences(result_text) if response_type == "text" else 0

    lexical_diversity = (len(result_words) / word_count) if word_count else 0.0
    query_term_coverage = (
        len(query_words.intersection(result_words)) / len(query_words)
        if query_words
        else 0.0
    )

    if response_type == "url":
        relevance_score = 0.5 if result_text else 0.0
        completeness_score = 1.0 if result_text else 0.0
        coherence_score = 1.0 if result_text else 0.0
    else:
        length_score = _clamp(word_count / 80)
        sentence_density = _clamp(sentence_count / 3)
        avg_sentence_len = word_count / max(sentence_count, 1)
        readability_score = _clamp(1 - abs(avg_sentence_len - 18) / 18)

        relevance_score = query_term_coverage
        completeness_score = _clamp((length_score * 0.7) + (sentence_density * 0.3))
        coherence_score = _clamp((lexical_diversity * 0.4) + (readability_score * 0.6))

    overall_score = _clamp(
        (relevance_score * 0.4)
        + (completeness_score * 0.3)
        + (coherence_score * 0.3)
    )

    return {
        "response_type": response_type,
        "overall_score": _round_metric(overall_score),
        "relevance_score": _round_metric(relevance_score),
        "completeness_score": _round_metric(completeness_score),
        "coherence_score": _round_metric(coherence_score),
        "lexical_diversity": _round_metric(lexical_diversity),
        "query_term_coverage": _round_metric(query_term_coverage),
        "word_count": word_count,
        "sentence_count": sentence_count,
        "char_count": char_count,
        "cached": cached,
    }
