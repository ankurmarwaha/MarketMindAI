def score_signal(name: str, change: float | None) -> int:
    if change is None:
        return 0

    # Rules:
    # Equities up = risk-on
    # VIX up = risk-off
    # Gold up = risk-off (defensive)
    # USD up = risk-off (flight to safety)
    # Bonds (10Y yield) down = risk-off (fear)

    if name == "S&P 500":
        return 1 if change > 0 else -1

    if name == "VIX":
        return -1 if change > 0 else 1

    if name == "Gold":
        return -1 if change > 0 else 1

    if name == "USD Index":
        return -1 if change > 0 else 1

    if name == "US 10Y Treasury":
        # Yield up = risk-on, yield down = risk-off
        return 1 if change > 0 else -1

    return 0


def compute_risk_regime(signals: dict):
    """
    signals: { name: change }
    """
    scores = {}
    total_score = 0

    for name, change in signals.items():
        s = score_signal(name, change)
        scores[name] = s
        total_score += s

    if total_score >= 2:
        regime = "🟢 Risk-On"
    elif total_score <= -2:
        regime = "🔴 Risk-Off"
    else:
        regime = "🟡 Neutral"

    return regime, total_score, scores


def explain_regime(regime: str, scores: dict):
    positives = [k for k, v in scores.items() if v > 0]
    negatives = [k for k, v in scores.items() if v < 0]

    if regime.startswith("🟢"):
        return (
            "Markets are showing risk-on behavior. Strength in assets like "
            f"{', '.join(positives)} suggests investors are comfortable taking risk."
        )
    elif regime.startswith("🔴"):
        return (
            "Markets are in risk-off mode. Defensive signals from "
            f"{', '.join(negatives)} indicate caution and capital preservation."
        )
    else:
        return (
            "Markets are mixed with no strong consensus. Some assets point to risk-taking "
            "while others suggest caution."
        )
