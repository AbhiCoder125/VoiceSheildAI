# VoiceShield AI – Risk Engine

## Overview

The VoiceShield risk engine combines the AI voice analysis result from Group 1
with caller, transaction, and contextual information to calculate an overall
security risk.

The engine does not rely on AI voice probability alone.

## Risk Factors

The final risk score uses four components:

- Voice Risk
- Caller Risk
- Transaction Risk
- Context Risk

## Scoring Weights

The prototype uses:

| Risk Factor | Weight |
|---|---:|
| Voice Risk | 40% |
| Caller Risk | 20% |
| Transaction Risk | 25% |
| Context Risk | 15% |

Final Score:

Final Score =
(Voice Risk × 0.40) +
(Caller Risk × 0.20) +
(Transaction Risk × 0.25) +
(Context Risk × 0.15)

These weights are prototype design parameters and should be validated
and tuned using additional test scenarios.

## Risk Levels

| Score | Risk Level |
|---:|---|
| 0–24 | LOW |
| 25–49 | MEDIUM |
| 50–74 | HIGH |
| 75–100 | CRITICAL |

## Voice Risk

Voice risk is derived from Group 1's `ai_probability`.

For example:

- 0.10 → low voice risk
- 0.50 → moderate voice risk
- 0.90 → high voice risk

## Caller Risk

Caller risk considers:

- Known or trusted caller
- Unknown caller
- Suspicious caller
- Caller type
- Claimed authority or executive identity

An unknown caller claiming to be a CEO or another authority increases the
risk significantly.

## Transaction Risk

Transaction risk considers:

- Whether a transaction is requested
- Transaction amount
- Financial requests
- Sensitive information requests

Higher-value transactions increase the security risk.

## Context Risk

Context risk considers:

- Urgency
- Authority impersonation
- Sensitive actions
- Unexpected situations

High urgency combined with suspicious circumstances increases the risk.

## Security Recommendations

| Risk Level | Recommendation |
|---|---|
| LOW | ALLOW |
| MEDIUM | WARN |
| HIGH | SECONDARY VERIFICATION |
| CRITICAL | BLOCK / ESCALATE |

## Explainability

The risk engine returns human-readable reasons explaining the risk decision.

Examples:

- Synthetic voice probability is high
- Caller identity is unknown
- Caller claims an authority identity
- Financial transaction requested
- High urgency detected

This allows the frontend to explain why an interaction was classified as risky.

## Required Test Scenarios

The risk engine was tested against the following scenarios:

1. Genuine voice + known caller → LOW
2. Synthetic voice + unknown caller → HIGH
3. Synthetic voice + CEO impersonation → HIGH/CRITICAL
4. Synthetic voice + financial fraud → CRITICAL
5. Synthetic voice + OTP/sensitive request + high urgency → HIGH/CRITICAL
6. Dangerous transaction scenario must not receive LOW risk

## Current Test Result

The complete repository test suite passes successfully.

Result:

`15 passed`
