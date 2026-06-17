import pandas as pd


REQUIRED_COLUMNS = [
    "date",
    "phone_hours",
    "sleep_quality",
    "mood",
    "deep_work_hours",
    "distraction_minutes",
    "primary_task"
]


def validate_dataframe(df):

    missing_columns = []

    for column in REQUIRED_COLUMNS:

        if column not in df.columns:

            missing_columns.append(column)

    if missing_columns:

        return {
            "valid": False,
            "message":
            f"Missing columns: {', '.join(missing_columns)}"
        }

    return {
        "valid": True,
        "message": "Validation successful."
    }
    
if __name__ == "__main__":

    sample_df = pd.DataFrame(
        columns=REQUIRED_COLUMNS
    )

    print(
        validate_dataframe(sample_df)
    )