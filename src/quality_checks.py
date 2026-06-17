import pandas as pd

def data_quality_report(df):

    total_records = len(df)

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicate_dates = int(
        df["date"].duplicated().sum()
    )

    invalid_phone_hours = int(
        ((df["phone_hours"] < 0) |
         (df["phone_hours"] > 24)).sum()
    )

    invalid_deep_work = int(
        ((df["deep_work_hours"] < 0) |
         (df["deep_work_hours"] > 24)).sum()
    )

    invalid_sleep = int(
        ((df["sleep_quality"] < 1) |
         (df["sleep_quality"] > 5)).sum()
    )

    invalid_mood = int(
        ((df["mood"] < 1) |
         (df["mood"] > 5)).sum()
    )

    invalid_distraction = int(
        ((df["distraction_minutes"] < 0) |
         (df["distraction_minutes"] > 1440)).sum()
    )

    issues = (
        missing_values
        + duplicate_dates
        + invalid_phone_hours
        + invalid_deep_work
        + invalid_sleep
        + invalid_mood
        + invalid_distraction
    )

    score = max(
        0,
        round(
            100 - ((issues / max(total_records, 1)) * 100),
            2
        )
    )

    return {
        "score": score,
        "missing_values": missing_values,
        "duplicate_dates": duplicate_dates,
        "invalid_phone_hours": invalid_phone_hours,
        "invalid_deep_work": invalid_deep_work,
        "invalid_sleep": invalid_sleep,
        "invalid_mood": invalid_mood,
        "invalid_distraction": invalid_distraction
    }