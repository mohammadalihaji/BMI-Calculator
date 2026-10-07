import sqlite3
from datetime import datetime

DB_FILE = "bmi_history.db"

def get_connection():
    """Returns a connection to the SQLite database with error handling."""
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def init_db():
    """Creates the 'bmi_records' table if it does not already exist."""
    conn = get_connection()
    if conn is None:
        return False

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bmi_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,
                    weight REAL NOT NULL,
                    height REAL NOT NULL,
                    bmi REAL NOT NULL,
                    category TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        return True
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        return False
    finally:
        conn.close()

def save_record(user_name, weight, height, bmi, category):
    """Saves a new BMI calculation record for a named user."""
    conn = get_connection()
    if conn is None:
        raise RuntimeError("Could not connect to database.")

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bmi_records (user_name, weight, height, bmi, category, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_name.strip(), weight, height, round(bmi, 2), category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        return True
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to save record: {e}")
    finally:
        conn.close()

def get_records_by_user(user_name):
    """Retrieves all historical BMI records for a specific user, ordered by date."""
    conn = get_connection()
    if conn is None:
        raise RuntimeError("Could not connect to database.")

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, user_name, weight, height, bmi, category, created_at
            FROM bmi_records
            WHERE LOWER(user_name) = LOWER(?)
            ORDER BY created_at ASC
        """, (user_name.strip(),))
        return cursor.fetchall()
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to fetch records: {e}")
    finally:
        conn.close()

def get_all_users():
    """Returns a list of all unique user names currently in the database."""
    conn = get_connection()
    if conn is None:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT user_name
            FROM bmi_records
            ORDER BY user_name ASC
        """)
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except sqlite3.Error as e:
        print(f"Error fetching users: {e}")
        return []
    finally:
        conn.close()

def delete_record(record_id):
    """Deletes a specific record by its primary key ID."""
    conn = get_connection()
    if conn is None:
        raise RuntimeError("Could not connect to database.")

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bmi_records WHERE id = ?", (record_id,))
        return True
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to delete record: {e}")
    finally:
        conn.close()
