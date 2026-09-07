import io

import pytest

from backend.app import create_app


@pytest.fixture
def client():

    app = create_app()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def send_request(
    client,
    caller_id,
    caller_type,
    claimed_identity,
    transaction_requested,
    transaction_amount,
    urgency,
    sensitive_information_requested
):

    return client.post(
        "/analyze",
        data={
            "audio": (
                io.BytesIO(b"fake audio"),
                "test.wav"
            ),
            "caller_id": caller_id,
            "caller_type": caller_type,
            "claimed_identity": claimed_identity,
            "transaction_requested":
                transaction_requested,
            "transaction_amount":
                transaction_amount,
            "urgency": urgency,
            "sensitive_information_requested":
                sensitive_information_requested
        },
        content_type="multipart/form-data"
    )


def test_normal_scenario(
    client,
    monkeypatch
):

    monkeypatch.setattr(
        "backend.routes.analyze.analyze_risk",
        lambda voice, context: {
            "risk_analysis": {
                "risk_score": 10,
                "risk_level": "LOW"
            },
            "risk_factors": {},
            "explanation": [],
            "recommendation": {}
        }
    )

    response = send_request(
        client,
        "user001",
        "known",
        "friend",
        "false",
        "0",
        "low",
        "false"
    )

    assert response.status_code == 200


def test_suspicious_scenario(
    client,
    monkeypatch
):

    monkeypatch.setattr(
        "backend.routes.analyze.analyze_risk",
        lambda voice, context: {
            "risk_analysis": {
                "risk_score": 90,
                "risk_level": "CRITICAL"
            },
            "risk_factors": {},
            "explanation": [],
            "recommendation": {}
        }
    )

    response = send_request(
        client,
        "unknown",
        "unknown",
        "CEO",
        "true",
        "500000",
        "high",
        "false"
    )

    assert response.status_code == 200