from analysis import load_data
import pandas as pd


def calculate_daily_scores(df):
    scores = []

    for i in range(7, len(df) + 1):

        window = df.iloc[i - 7:i]

        avg_focus = window["deep_work_hours"].mean()
        avg_phone = window["phone_hours"].mean()
        avg_sleep = window["sleep_quality"].mean()
        avg_mood = window["mood"].mean()

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

        scores.append(
            {
                "date": window.iloc[-1]["date"],
                "productivity_score": round(final_score, 2)
            }
        )

    return pd.DataFrame(scores)


if __name__ == "__main__":
    df = load_data()

    score_df = calculate_daily_scores(df)

    print(score_df.head())

    print("\n")

    print(score_df.tail())