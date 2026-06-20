def generate_intelligence_report(
    report,
    factor_analysis,
    ml_results,
    burnout
):

    insights = []

    # -------------------------
    # Productivity Status
    # -------------------------

    score = report["score"]

    if score < 50:
        insights.append(
            "Your productivity is currently low. Focus on improving your daily habits."
        )

    elif score < 70:
        insights.append(
            "Your productivity is average. Small improvements can create significant gains."
        )

    else:
        insights.append(
            "Your productivity is performing well. Maintain your current routine."
        )


    # -------------------------
    # Primary Limiter
    # -------------------------

    limiter = factor_analysis["weakest_factor"]


    if limiter == "Phone Usage":

        insights.append(
            "Reduce daily phone usage and create distraction-free deep work sessions."
        )


    elif limiter == "Focus":

        insights.append(
            "Increase dedicated deep work time and avoid multitasking."
        )


    elif limiter == "Sleep":

        insights.append(
            "Improve sleep quality to support better concentration and energy."
        )


    elif limiter == "Mood":

        insights.append(
            "Track activities that improve your mood and mental energy."
        )


    # -------------------------
    # ML Prediction
    # -------------------------

    if ml_results:

        prediction = ml_results["predicted_score"]

        if prediction < score:

            insights.append(
                "Your future productivity is predicted to decline. Take corrective action today."
            )

        else:

            insights.append(
                "Your productivity trend looks stable or improving."
            )


    # -------------------------
    # Burnout Intelligence
    # -------------------------

    risk = burnout["risk_level"]


    if risk == "High":

        insights.append(
            "High burnout risk detected. Reduce workload and prioritize recovery."
        )


    elif risk == "Medium":

        insights.append(
            "Moderate burnout risk detected. Maintain balance between work and rest."
        )


    else:

        insights.append(
            "Burnout risk is low. Your current work-recovery balance is healthy."
        )


    return {
        "insights": insights
    }