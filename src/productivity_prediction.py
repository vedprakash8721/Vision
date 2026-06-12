import pandas as pd
from sklearn.linear_model import LinearRegression
from metrics import calculate_score_history


def predict_next_productivity_score(df):

    score_history = calculate_score_history(df)

    if len(score_history) < 10:
        return None

    score_history = score_history.reset_index(drop=True)

    score_history["day_number"] = range(
        1,
        len(score_history) + 1
    )

    X = score_history[["day_number"]]

    y = score_history["productivity_score"]

    model = LinearRegression()

    model.fit(X, y)

    next_day = [[len(score_history) + 1]]

    prediction = model.predict(
        next_day
    )[0]

    prediction = max(
        0,
        min(
            100,
            round(prediction, 2)
        )
    )

    return prediction