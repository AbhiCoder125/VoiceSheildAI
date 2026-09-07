from backend.services.voice_service import (
    get_mock_voice_result,
    validate_voice_result
)


def test_mock_voice_result():

    result = get_mock_voice_result()

    assert "classification" in result

    assert "ai_probability" in result

    assert "human_probability" in result


def test_voice_probability_range():

    result = get_mock_voice_result()

    assert 0 <= result["ai_probability"] <= 1

    assert 0 <= result["human_probability"] <= 1


def test_voice_result_validation():

    result = {
        "classification": "synthetic",
        "ai_probability": 0.91,
        "human_probability": 0.09
    }

    assert validate_voice_result(result)