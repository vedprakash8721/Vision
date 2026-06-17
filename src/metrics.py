from analysis import load_data
import pandas as pd


def get_last_7_day_metrics(df):
    recent = df.tail(7)

    return {
        "avg_focus": float(round(recent["deep_work_hours"].mean(), 2)),
        "avg_phone": float(round(recent["phone_hours"].mean(), 2)),
        "avg_sleep": float(round(recent["sleep_quality"].mean(), 2)),
        "avg_mood": float(round(recent["mood"].mean(), 2))
    }

def get_score_components(df):

    metrics = get_last_7_day_metrics(df)

    focus_score = min(
        (metrics["avg_focus"] / 8) * 100,
        100
    )

    phone_score = max(
        0,
        100 - (metrics["avg_phone"] / 6) * 100
    )

    sleep_score = (
        metrics["avg_sleep"] / 5
    ) * 100

    mood_score = (
        metrics["avg_mood"] / 5
    ) * 100

    return {
        "focus_score": round(focus_score, 2),
        "phone_score": round(phone_score, 2),
        "sleep_score": round(sleep_score, 2),
        "mood_score": round(mood_score, 2)
    }
def get_primary_productivity_factor(df):

    scores = get_score_components(df)

    factors = {
        "Focus": scores["focus_score"],
        "Phone Usage": scores["phone_score"],
        "Sleep": scores["sleep_score"],
        "Mood": scores["mood_score"]
    }

    strongest_factor = max(
        factors,
        key=factors.get
    )

    weakest_factor = min(
        factors,
        key=factors.get
    )

    return {
        "strongest_factor": strongest_factor,
        "weakest_factor": weakest_factor,
        "scores": factors
    }

def calculate_productivity_score(df):

    scores = get_score_components(df)

    final_score = (
        0.40 * scores["focus_score"]
        + 0.20 * scores["phone_score"]
        + 0.20 * scores["sleep_score"]
        + 0.20 * scores["mood_score"]
    )

    return round(final_score, 2)

def productivity_category(score):

    if score >= 85:
        return "Excellent"

    if score >= 70:
        return "Good"

    if score >= 50:
        return "Average"

    return "Poor"


def calculate_score_history(df):

    scores = []

    for i in range(7, len(df) + 1):

        window = df.iloc[i - 7:i]

        metrics = get_last_7_day_metrics(window)

        focus_score = min(
            (metrics["avg_focus"] / 8) * 100,
            100
        )

        phone_score = max(
            0,
            100 - (metrics["avg_phone"] / 6) * 100
        )

        sleep_score = (
            metrics["avg_sleep"] / 5
        ) * 100

        mood_score = (
            metrics["avg_mood"] / 5
        ) * 100

        final_score = (
            0.40 * focus_score
            + 0.20 * phone_score
            + 0.20 * sleep_score
            + 0.20 * mood_score
        )

        scores.append(
            {
                "date": window.iloc[-1]["date"],
                "productivity_score": round(final_score, 2)
            }
        )

    return pd.DataFrame(scores)


if __name__ == "__main__":

    df = load_data()

    metrics = get_last_7_day_metrics(df)

    score = calculate_productivity_score(df)

    category = productivity_category(score)

    print(metrics)

    print(f"\nScore: {score}")

    print(f"Category: {category}")

    print()

    print(
        get_primary_productivity_factor(df)
    )