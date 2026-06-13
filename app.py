import streamlit as st
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path
from datetime import date

# Add src folder to path
sys.path.append(str(Path(__file__).parent / "src"))

from quality_checks import data_quality_report
from productivity_prediction import (
    predict_next_productivity_score
)
from productivity_prediction_v2 import (
    train_prediction_models
)
from analysis import load_data
from metrics import (
    calculate_score_history,
    get_primary_productivity_factor
)

from rules_engine import generate_report

from db_manager import (
    insert_single_record,
    insert_dataframe,
    get_total_records,
    get_latest_date,
    get_date_range,
    get_record_by_date,
    update_record,
    delete_record
)

from data_validation import validate_dataframe

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Vision Dashboard",
    page_icon="🚀",
    layout="wide"
)

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("🚀 Vision")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Daily Log",
        "Upload CSV",
        "Edit Records",
        "Delete Records"
    ]
)

# --------------------------------------------------
# ADD DAILY LOG PAGE
# --------------------------------------------------

if page == "Add Daily Log":

    st.title("➕ Add Daily Productivity Log")

    with st.form("daily_log_form"):

        log_date = st.date_input(
            "Date",
            value=date.today()
        )

        phone_hours = st.number_input(
            "Phone Hours",
            min_value=0.0,
            max_value=24.0,
            value=2.0,
            step=0.5
        )

        sleep_quality = st.slider(
            "Sleep Quality",
            1,
            5,
            3
        )

        mood = st.slider(
            "Mood",
            1,
            5,
            3
        )

        deep_work_hours = st.number_input(
            "Deep Work Hours",
            min_value=0.0,
            max_value=24.0,
            value=4.0,
            step=0.5
        )

        distraction_minutes = st.number_input(
            "Distraction Minutes",
            min_value=0,
            max_value=1440,
            value=60
        )

        primary_task = st.selectbox(
            "Primary Task",
            [
                "ML Study",
                "NLP",
                "Practice Interview Ques",
                "Revision",
                "Work on Project"
            ]
        )

        submit = st.form_submit_button(
            "Save Entry"
        )

    if submit:

        record = {
            "date": str(log_date),
            "phone_hours": phone_hours,
            "sleep_quality": sleep_quality,
            "mood": mood,
            "deep_work_hours": deep_work_hours,
            "distraction_minutes": distraction_minutes,
            "primary_task": primary_task
        }

        insert_single_record(record)

        st.success(
            "Entry saved successfully."
        )

        st.rerun()

    st.stop()

# --------------------------------------------------
# UPLOAD CSV PAGE
# --------------------------------------------------

if page == "Upload CSV":

    st.title("📤 Upload Productivity CSV")

    uploaded_file = st.file_uploader(
        "Choose CSV File",
        type=["csv"]
    )

    if uploaded_file is not None:

        uploaded_df = pd.read_csv(
            uploaded_file
        )

        validation = validate_dataframe(
            uploaded_df
        )

        if validation["valid"]:

            st.success(
                "CSV validation passed."
            )

            st.dataframe(
                uploaded_df.head(),
                use_container_width=True
            )

            if st.button(
                "Import CSV Into Database"
            ):

                insert_dataframe(
                    uploaded_df
                )

                st.success(
                    "CSV imported successfully."
                )

                st.rerun()

        else:

            st.error(
                validation["message"]
            )

    st.stop()
# --------------------------------------------------
# EDIT RECORDS PAGE
# --------------------------------------------------

if page == "Edit Records":

    st.title("✏️ Edit Productivity Record")

    df_records = load_data()

    available_dates = (
        df_records["date"]
        .sort_values(ascending=False)
        .tolist()
    )

    selected_date = st.selectbox(
        "Select Record Date",
        available_dates
    )

    record = get_record_by_date(
        selected_date
    )

    if record:

        with st.form("edit_record_form"):

            phone_hours = st.number_input(
                "Phone Hours",
                min_value=0.0,
                max_value=24.0,
                value=float(record["phone_hours"]),
                step=0.5
            )

            sleep_quality = st.slider(
                "Sleep Quality",
                1,
                5,
                int(record["sleep_quality"])
            )

            mood = st.slider(
                "Mood",
                1,
                5,
                int(record["mood"])
            )

            deep_work_hours = st.number_input(
                "Deep Work Hours",
                min_value=0.0,
                max_value=24.0,
                value=float(record["deep_work_hours"]),
                step=0.5
            )

            distraction_minutes = st.number_input(
                "Distraction Minutes",
                min_value=0,
                max_value=1440,
                value=int(record["distraction_minutes"])
            )

            task_options = [
                "ML Study",
                "NLP",
                "Practice Interview Ques",
                "Revision",
                "Work on Project"
            ]

            primary_task = st.selectbox(
                "Primary Task",
                task_options,
                index=task_options.index(
                    record["primary_task"]
                )
            )

            update_btn = st.form_submit_button(
                "Update Record"
            )

        if update_btn:

            updated_record = {
                "date": selected_date,
                "phone_hours": phone_hours,
                "sleep_quality": sleep_quality,
                "mood": mood,
                "deep_work_hours": deep_work_hours,
                "distraction_minutes": distraction_minutes,
                "primary_task": primary_task
            }

            update_record(
                updated_record
            )

            st.success(
                "Record updated successfully."
            )

            st.rerun()

    st.stop()

# --------------------------------------------------
# DELETE RECORDS PAGE
# --------------------------------------------------

if page == "Delete Records":

    st.title("🗑️ Delete Productivity Record")

    df_records = load_data()

    available_dates = (
        df_records["date"]
        .sort_values(ascending=False)
        .tolist()
    )

    selected_date = st.selectbox(
        "Select Record To Delete",
        available_dates
    )

    record = get_record_by_date(
        selected_date
    )

    if record:

        st.subheader("Record Preview")

        st.write(record)

        confirm_delete = st.checkbox(
            "I understand this action cannot be undone."
        )

        if st.button(
            "Delete Record",
            type="primary"
        ):

            if confirm_delete:

                delete_record(
                    selected_date
                )

                st.success(
                    "Record deleted successfully."
                )

                st.rerun()

            else:

                st.warning(
                    "Please confirm deletion."
                )

    st.stop()

# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------

df = load_data()

if len(df) == 0:

    st.warning(
        "No data available."
    )

    st.stop()

# --------------------------------------------------
# DATA CHECK
# --------------------------------------------------

if len(df) < 7:

    st.warning(
        f"Only {len(df)} records found. "
        "At least 7 records are recommended for reliable trend analysis."
    )

# --------------------------------------------------
# ANALYTICS
# --------------------------------------------------

report = generate_report(df)

score_history = calculate_score_history(df)

factor_analysis = get_primary_productivity_factor(df)

quality_report = data_quality_report(df)

predicted_score = (
    predict_next_productivity_score(df)
)
ml_results = train_prediction_models(df)
# --------------------------------------------------
# DATABASE STATS
# --------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.subheader(
    "📂 Database Stats"
)

total_records = get_total_records()

latest_date = get_latest_date()

start_date, end_date = get_date_range()

st.sidebar.metric(
    "Total Records",
    total_records
)

st.sidebar.write(
    f"Latest Entry: {latest_date}"
)

st.sidebar.write(
    f"Range: {start_date} → {end_date}"
)

st.sidebar.markdown("---")

# --------------------------------------------------
# DASHBOARD METRICS
# --------------------------------------------------

st.sidebar.metric(
    "Productivity Score",
    f"{report['score']}/100"
)

st.sidebar.metric(
    "Category",
    report["category"]
)

st.sidebar.metric(
    "Weekly Change",
    f"{report['trend']['change_percent']}%"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title(
    "🚀 Vision - Productivity Intelligence Dashboard"
)

st.caption(
    "Analyze productivity behavior and generate actionable insights."
)

st.markdown("---")

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

with col1:
    st.metric(
        "Productivity Score",
        f"{report['score']}/100"
    )

with col2:
    st.metric(
        "Category",
        report["category"]
    )

with col3:
    st.metric(
        "Strongest Factor",
        report["strongest_factor"]
    )

with col4:
    st.metric(
        "Primary Limiter",
        report["weakest_factor"]
    )
with col5:
    st.metric(
        "Data Health",
        f"{quality_report['score']}%"
    )
with col6:

    prediction_text = (
        predicted_score
        if predicted_score is not None
        else "N/A"
    )
with col7:

    st.metric(
        "Best Model",
        (
            ml_results["best_model"]
            if ml_results
            else "N/A"
        )
    )

with col8:

    st.metric(
        "R² Score",
        (
            ml_results["r2_score"]
            if ml_results
            else "N/A"
        )
    )
    st.metric(
        "Predicted Score",
        prediction_text
    )
st.markdown("---")

# --------------------------------------------------
# EXECUTIVE SUMMARY
# --------------------------------------------------

st.subheader("📌 Executive Summary")

st.write(
    f"**Weekly Change:** {report['trend']['change_percent']}%"
)

st.write(
    f"**Summary:** {report['summary']}"
)

st.success(
    f"Recommendation: {report['recommendation']}"
)
if ml_results:

    st.info(
        f"""
Best Model: {ml_results['best_model']}

R² Score: {ml_results['r2_score']}

MAE: {ml_results['mae']}

Predicted Future Productivity:
{ml_results['predicted_score']}
"""
    )
st.markdown("---")

# --------------------------------------------------
# PRODUCTIVITY TREND
# --------------------------------------------------

st.subheader("📈 Productivity Trend")

trend_fig = px.line(
    score_history,
    x="date",
    y="productivity_score",
    markers=True,
    title="Productivity Score Over Time"
)

st.plotly_chart(
    trend_fig,
    use_container_width=True
)

# --------------------------------------------------
# PRODUCTIVITY FACTOR BREAKDOWN
# --------------------------------------------------

st.subheader("📊 Productivity Factor Breakdown")

factor_df = pd.DataFrame({
    "Factor": list(
        factor_analysis["scores"].keys()
    ),
    "Score": list(
        factor_analysis["scores"].values()
    )
})

factor_fig = px.bar(
    factor_df,
    x="Factor",
    y="Score",
    text="Score",
    title="Productivity Component Scores"
)

factor_fig.update_traces(
    textposition="outside"
)

factor_fig.update_layout(
    yaxis_range=[0, 100]
)

st.plotly_chart(
    factor_fig,
    use_container_width=True
)


# ==================================================
# PASTE DATA QUALITY REPORT HERE
# ==================================================

st.markdown("---")

st.subheader("🛡️ Data Quality Report")

quality_df = pd.DataFrame({
    "Metric": [
        "Missing Values",
        "Duplicate Dates",
        "Invalid Phone Hours",
        "Invalid Deep Work",
        "Invalid Sleep",
        "Invalid Mood",
        "Invalid Distraction"
    ],
    "Count": [
        quality_report["missing_values"],
        quality_report["duplicate_dates"],
        quality_report["invalid_phone_hours"],
        quality_report["invalid_deep_work"],
        quality_report["invalid_sleep"],
        quality_report["invalid_mood"],
        quality_report["invalid_distraction"]
    ]
})

st.dataframe(
    quality_df,
    use_container_width=True
)

# --------------------------------------------------
# DATASET
# --------------------------------------------------

st.subheader("📋 Dataset Preview")

st.dataframe(
    df,
    use_container_width=True
)
