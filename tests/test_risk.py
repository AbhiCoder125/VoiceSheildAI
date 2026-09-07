from risk_engine.risk_engine import calculate_risk


def test_genuine_known_caller():
    voice_result = {
        "classification": "genuine",
        "ai_probability": 0.05
    }

    context = {
        "caller_id": "known",
        "caller_type": "trusted",
        "claimed_identity": None,
        "transaction_requested": False,
        "transaction_amount": 0,
        "urgency": "low",
        "sensitive_information_requested": False
    }

    result = calculate_risk(voice_result, context)

    assert result["risk_level"] == "LOW"
    assert result["risk_score"] < 25


def test_synthetic_voice_only():
    voice_result = {
        "classification": "synthetic",
        "ai_probability": 0.90
    }

    context = {
        "caller_id": "unknown",
        "caller_type": "unknown",
        "claimed_identity": None,
        "transaction_requested": False,
        "transaction_amount": 0,
        "urgency": "low",
        "sensitive_information_requested": False
    }

    result = calculate_risk(voice_result, context)

    assert result["risk_level"] == "HIGH"


def test_synthetic_ceo_impersonation():
    voice_result = {
        "classification": "synthetic",
        "ai_probability": 0.90
    }

    context = {
        "caller_id": "unknown",
        "caller_type": "unknown",
        "claimed_identity": "CEO",
        "transaction_requested": False,
        "transaction_amount": 0,
        "urgency": "high",
        "sensitive_information_requested": False
    }

    result = calculate_risk(voice_result, context)

    assert result["risk_level"] in ["HIGH", "CRITICAL"]


def test_synthetic_financial_fraud():
    voice_result = {
        "classification": "synthetic",
        "ai_probability": 0.90
    }

    context = {
        "caller_id": "unknown",
        "caller_type": "unknown",
        "claimed_identity": "CEO",
        "transaction_requested": True,
        "transaction_amount": 500000,
        "urgency": "high",
        "sensitive_information_requested": False
    }

    result = calculate_risk(voice_result, context)

    assert result["risk_level"] == "CRITICAL"


def test_otp_attack():
    voice_result = {
        "classification": "synthetic",
        "ai_probability": 0.90
    }

    context = {
        "caller_id": "unknown",
        "caller_type": "unknown",
        "claimed_identity": None,
        "transaction_requested": False,
        "transaction_amount": 0,
        "urgency": "high",
        "sensitive_information_requested": True
    }

    result = calculate_risk(voice_result, context)

    assert result["risk_level"] in ["HIGH", "CRITICAL"]


def test_dangerous_case_never_low():
    voice_result = {
        "classification": "synthetic",
        "ai_probability": 0.90
    }

    context = {
        "caller_id": "unknown",
        "caller_type": "unknown",
        "claimed_identity": "CEO",
        "transaction_requested": True,
        "transaction_amount": 1000000,
        "urgency": "very high",
        "sensitive_information_requested": False
    }

    result = calculate_risk(voice_result, context)

    assert result["risk_level"] != "LOW"
    assert result["risk_score"] >= 50