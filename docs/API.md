# VoiceShield AI API

## Base URL

http://localhost:5000

---

# GET /health

Checks whether the backend is running.

## Request

GET /health

## Response

```json
{
    "status": "ok",
    "service": "VoiceShield AI",
    "version": "stage-1"
}