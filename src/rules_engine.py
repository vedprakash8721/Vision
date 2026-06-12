from analysis import load_data

from metrics import (
    calculate_productivity_score,
    productivity_category,
    calculate_score_history,
    get_primary_productivity_factor
)

from trend_analysis import analyze_trend


def generate_report(df):

    score = calculate_productivity_score(df)

    category = productivity_category(score)

    score_df = calculate_score_history(df)

    trend = analyze_trend(score_df)

    factor_analysis = get_primary_productivity_factor(df)

    strongest_factor = factor_analysis["strongest_factor"]

    weakest_factor = factor_analysis["weakest_factor"]

    # Trend Summary
    if trend["change_percent"] > 5:
        summary = (
            f"Productivity improved by "
            f"{trend['change_percent']}% this week."
        )

    elif trend["change_percent"] < -5:
        summary = (
            f"Productivity declined by "
            f"{abs(trend['change_percent'])}% this week."
        )

    else:
        summary = (
            "Productivity remained relatively stable this week."
        )

    # Recommendation Engine
    recommendations = {
        "Phone Usage":
        "Reducing phone usage may provide the largest productivity improvement.",

        "Focus":
        "Increasing deep work hours should be your top priority.",

        "Sleep":
        "Improving sleep quality may positively impact overall productivity.",

        "Mood":
        "Improving mood and mental well-being may improve performance."
    }

    recommendation = recommendations.get(
        weakest_factor,
        "Continue maintaining current productivity habits."
    )

    return {
        "score": score,
        "category": category,
        "trend": trend,
        "summary": summary,
        "strongest_factor": strongest_factor,
        "weakest_factor": weakest_factor,
        "recommendation": recommendation
    }


if __name__ == "__main__":

    df = load_data()

    report = generate_report(df)

    print("\n===== PRODUCTIVITY REPORT =====\n")

    print(
        f"Productivity Score : "
        f"{report['score']}/100"
    )

    print(
        f"Category           : "
        f"{report['category']}"
    )

    print(
        f"Weekly Change      : "
        f"{report['trend']['change_percent']}%"
    )

    print()

    print(
        f"Strongest Factor   : "
        f"{report['strongest_factor']}"
    )

    print(
        f"Primary Limiter    : "
        f"{report['weakest_factor']}"
    )

    print()

    print("Summary:")

    print(
        report['summary']
    )

    print()

    print("Recommendation:")

    print(
        report['recommendation']
    )