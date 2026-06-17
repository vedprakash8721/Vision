import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression

from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    r2_score
)

from metrics import calculate_productivity_score


def prepare_ml_dataset(df):

    rows = []

    for i in range(7, len(df)):

        history = df.iloc[:i]

        score = calculate_productivity_score(
            history
        )

        current_row = df.iloc[i]

        rows.append({
            "phone_hours":
                current_row["phone_hours"],

            "sleep_quality":
                current_row["sleep_quality"],

            "mood":
                current_row["mood"],

            "deep_work_hours":
                current_row["deep_work_hours"],

            "distraction_minutes":
                current_row["distraction_minutes"],

            "target_score":
                score
        })

    return pd.DataFrame(rows)


def train_prediction_models(df):

    ml_df = prepare_ml_dataset(df)

    if len(ml_df) < 30:
        return None

    X = ml_df[
        [
            "phone_hours",
            "sleep_quality",
            "mood",
            "deep_work_hours",
            "distraction_minutes"
        ]
    ]

    y = ml_df["target_score"]

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )
    )

    # -------------------------
    # Linear Regression
    # -------------------------

    lr_model = LinearRegression()

    lr_model.fit(
        X_train,
        y_train
    )

    lr_preds = lr_model.predict(
        X_test
    )

    lr_r2 = r2_score(
        y_test,
        lr_preds
    )

    lr_mae = mean_absolute_error(
        y_test,
        lr_preds
    )

    # -------------------------
    # Random Forest
    # -------------------------

    rf_model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    rf_model.fit(
        X_train,
        y_train
    )

    rf_preds = rf_model.predict(
        X_test
    )

    rf_r2 = r2_score(
        y_test,
        rf_preds
    )

    rf_mae = mean_absolute_error(
        y_test,
        rf_preds
    )

    # -------------------------
    # Best Model Selection
    # -------------------------

    if rf_r2 > lr_r2:

        best_model = rf_model

        best_model_name = (
            "Random Forest"
        )

        best_r2 = rf_r2

        best_mae = rf_mae

    else:

        best_model = lr_model

        best_model_name = (
            "Linear Regression"
        )

        best_r2 = lr_r2

        best_mae = lr_mae

    latest_row = df.iloc[-1]

    future_features = pd.DataFrame(
        [{
            "phone_hours":
                latest_row["phone_hours"],

            "sleep_quality":
                latest_row["sleep_quality"],

            "mood":
                latest_row["mood"],

            "deep_work_hours":
                latest_row["deep_work_hours"],

            "distraction_minutes":
                latest_row[
                    "distraction_minutes"
                ]
        }]
    )

    predicted_score = (
        best_model.predict(
            future_features
        )[0]
    )

    predicted_score = round(
        predicted_score,
        2
    )

    return {
        "predicted_score":
            predicted_score,

        "best_model":
            best_model_name,

        "r2_score":
            round(best_r2, 3),

        "mae":
            round(best_mae, 2)
    }