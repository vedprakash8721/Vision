from analysis import load_data
from metrics import calculate_score_history


def analyze_trend(score_df):

    current_week = score_df.tail(7)

    previous_week = score_df.iloc[-14:-7]

    current_avg = current_week["productivity_score"].mean()

    previous_avg = previous_week["productivity_score"].mean()

    change_percent = (
        (current_avg - previous_avg)
        / previous_avg
    ) * 100

    return {
        "current_week_score": round(current_avg, 2),
        "previous_week_score": round(previous_avg, 2),
        "change_percent": round(change_percent, 2)
    }


if __name__ == "__main__":

    df = load_data()

    score_df = calculate_score_history(df)

    trend = analyze_trend(score_df)

    print("\n===== PRODUCTIVITY TREND =====\n")

    print(
        f"Previous Week Score : "
        f"{trend['previous_week_score']}"
    )

    print(
        f"Current Week Score  : "
        f"{trend['current_week_score']}"
    )

    print(
        f"Change (%)          : "
        f"{trend['change_percent']}%"
    )