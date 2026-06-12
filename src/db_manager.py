import sqlite3
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# DATABASE PATH
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "focusiq.db"

# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_connection():
    return sqlite3.connect(DB_PATH)

# --------------------------------------------------
# CREATE TABLE
# --------------------------------------------------

def create_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_logs (
            date TEXT PRIMARY KEY,
            phone_hours REAL,
            sleep_quality INTEGER,
            mood INTEGER,
            deep_work_hours REAL,
            distraction_minutes INTEGER,
            primary_task TEXT
        )
    """)

    conn.commit()
    conn.close()

# --------------------------------------------------
# CSV IMPORT
# --------------------------------------------------

def insert_from_csv(csv_path):

    df = pd.read_csv(csv_path)

    conn = get_connection()

    df.to_sql(
        "daily_logs",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()
    conn.close()

    print("CSV data inserted successfully.")

# --------------------------------------------------
# SINGLE RECORD INSERT
# --------------------------------------------------

def insert_single_record(record):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO daily_logs
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            record["date"],
            record["phone_hours"],
            record["sleep_quality"],
            record["mood"],
            record["deep_work_hours"],
            record["distraction_minutes"],
            record["primary_task"]
        )
    )

    conn.commit()
    conn.close()

# --------------------------------------------------
# DATAFRAME INSERT
# --------------------------------------------------

def insert_dataframe(df):

    conn = get_connection()

    df.to_sql(
        "daily_logs",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()
    conn.close()

# --------------------------------------------------
# CHECK IF RECORD EXISTS
# --------------------------------------------------

def record_exists(date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM daily_logs
        WHERE date = ?
        """,
        (date,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None

# --------------------------------------------------
# TOTAL RECORD COUNT
# --------------------------------------------------

def get_total_records():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM daily_logs"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count

# --------------------------------------------------
# LATEST DATE
# --------------------------------------------------

def get_latest_date():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT MAX(date) FROM daily_logs"
    )

    latest_date = cursor.fetchone()[0]

    conn.close()

    return latest_date

# --------------------------------------------------
# DATE RANGE
# --------------------------------------------------

def get_date_range():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            MIN(date),
            MAX(date)
        FROM daily_logs
        """
    )

    start_date, end_date = cursor.fetchone()

    conn.close()

    return start_date, end_date

# --------------------------------------------------
# FETCH SAMPLE DATA
# --------------------------------------------------

def fetch_sample(limit=5):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM daily_logs
        ORDER BY date
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows
def get_record_by_date(selected_date):

    conn = get_connection()

    query = """
    SELECT *
    FROM daily_logs
    WHERE date = ?
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(selected_date,)
    )

    conn.close()

    if len(df) == 0:
        return None

    return df.iloc[0].to_dict()


def update_record(record):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE daily_logs
        SET
            phone_hours = ?,
            sleep_quality = ?,
            mood = ?,
            deep_work_hours = ?,
            distraction_minutes = ?,
            primary_task = ?
        WHERE date = ?
        """,
        (
            record["phone_hours"],
            record["sleep_quality"],
            record["mood"],
            record["deep_work_hours"],
            record["distraction_minutes"],
            record["primary_task"],
            record["date"]
        )
    )
def delete_record(selected_date):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM daily_logs
        WHERE date = ?
        """,
        (selected_date,)
    )

    conn.commit()
    conn.close()

# --------------------------------------------------
# TESTING
# --------------------------------------------------

if __name__ == "__main__":

    create_table()

    print(f"\nTotal Records: {get_total_records()}")

    print("\nSample Rows:\n")

    for row in fetch_sample():
        print(row)