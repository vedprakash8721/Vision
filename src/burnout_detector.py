def detect_burnout_risk(df):

    recent = df.tail(14)

    avg_sleep = recent["sleep_quality"].mean()

    avg_mood = recent["mood"].mean()

    avg_deep_work = recent[
        "deep_work_hours"
    ].mean()

    avg_distraction = recent[
        "distraction_minutes"
    ].mean()

    risk_score = 0

    if avg_sleep < 2.5:
        risk_score += 25

    if avg_mood < 2.5:
        risk_score += 25

    if avg_deep_work > 8:
        risk_score += 25

    if avg_distraction > 180:
        risk_score += 25

    if risk_score >= 75:

        level = "High"

    elif risk_score >= 40:

        level = "Medium"

    else:

        level = "Low"

    return {
        "risk_score": risk_score,
        "risk_level": level,
        "avg_sleep": round(avg_sleep, 2),
        "avg_mood": round(avg_mood, 2),
        "avg_deep_work": round(avg_deep_work, 2),
        "avg_distraction": round(avg_distraction, 2)
    }