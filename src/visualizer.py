import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from analysis import load_data
from metrics import calculate_score_history


def create_productivity_trend_chart():

    df = load_data()

    score_df = calculate_score_history(df)

    plt.figure(figsize=(10, 5))

    plt.plot(
        score_df["date"],
        score_df["productivity_score"]
    )

    plt.title("Productivity Score Trend")

    plt.xlabel("Date")

    plt.ylabel("Productivity Score")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        "visuals/productivity_score_trend.png"
    )

    print(
        "Chart saved to visuals/productivity_score_trend.png"
    )
def create_correlation_heatmap():

    df = load_data()

    columns = [
        "phone_hours",
        "sleep_quality",
        "mood",
        "deep_work_hours",
        "distraction_minutes"
    ]

    correlation_matrix = df[columns].corr()

    plt.figure(figsize=(8, 6))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="coolwarm"
    )

    plt.title(
        "Productivity Factors Correlation Heatmap"
    )

    plt.tight_layout()

    plt.savefig(
        "visuals/correlation_heatmap.png"
    )

    print(
        "Heatmap saved to visuals/correlation_heatmap.png"
    )

if __name__ == "__main__":

    create_productivity_trend_chart()

    create_correlation_heatmap()