import io

import pytest

from backend.app import create_app


@pytest.fixture
def client():

    app = create_app()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health(client):

    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"

    assert data["service"] == "VoiceShield AI"


def test_missing_audio(client):

    response = client.post(
        "/analyze",
        data={
            "caller_id": "unknown"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "error" in data


def test_invalid_audio_format(client):

    response = client.post(
        "/analyze",
        data={
            "audio": (
                io.BytesIO(b"fake file"),
                "test.txt"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400


def test_analyze_endpoint(client, monkeypatch):

    # Fake risk-engine result so this test
    # tests only Member 3's API.

    def fake_risk(
        voice_result,
        context
    ):

        return {
            "risk_analysis": {
                "risk_score": 20,
                "risk_level": "LOW"
            },
            "risk_factors": {},
            "explanation": [],
            "recommendation": {}
        }

    monkeypatch.setattr(
        "backend.routes.analyze.analyze_risk",
        fake_risk
    )

    response = client.post(
        "/analyze",
        data={
            "audio": (
                io.BytesIO(b"fake audio"),
                "test.wav"
            ),
            "caller_id": "user001",
            "caller_type": "known",
            "claimed_identity": "friend",
            "transaction_requested": "false",
            "transaction_amount": "0",
            "urgency": "low",
            "sensitive_information_requested": "false"
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "voice_analysis" in data

    assert "risk_analysis" in data

    assert "risk_factors" in data

    assert "explanation" in data

    assert "recommendation" in data