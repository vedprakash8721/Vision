from analysis import load_data


def calculate_productivity_score(df):
    recent = df.tail(7)

    avg_focus = recent["deep_work_hours"].mean()
    avg_phone = recent["phone_hours"].mean()
    avg_sleep = recent["sleep_quality"].mean()
    avg_mood = recent["mood"].mean()

    focus_score = min((avg_focus / 8) * 100, 100)

    phone_score = max(0, 100 - (avg_phone / 6) * 100)

    sleep_score = (avg_sleep / 5) * 100

    mood_score = (avg_mood / 5) * 100

    final_score = (
        0.40 * focus_score
        + 0.20 * phone_score
        + 0.20 * sleep_score
        + 0.20 * mood_score
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


if __name__ == "__main__":
    df = load_data()

    score = calculate_productivity_score(df)

    category = productivity_category(score)

    print("\n----- PRODUCTIVITY SCORE -----")
    print(f"Score     : {score}/100")
    print(f"Category  : {category}")