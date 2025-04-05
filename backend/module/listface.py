import json
import mysql.connector
import os
from dotenv import load_dotenv  # ✅ Load environment variables
from backend.module.logger import get_logger
logger = get_logger()
import streamlit as st  # ✅ Streamlit for web app
# ✅ Load environment variables from .env file
load_dotenv()

LIST_JSON_FILE = os.path.join(os.path.dirname(__file__), "jsons", "list.json")


def load_list_json():
    """Loads the name and email from list.json."""
    try:
        with open(LIST_JSON_FILE, "r") as file:
            data = json.load(file)
            user_info = data.get("user_info", [])
            if user_info:
                return user_info[0]["name"], user_info[0]["mail_id"]
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None
    return None, None


def save_list_json(name, email):
    """Overwrites the list.json file with the latest details only."""
    data = {"user_info": [{"name": name, "mail_id": email}]}
    with open(LIST_JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)


def fetch_database_data():
    """Fetches face data from the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host=st.secrets.mysql.host,  # ✅ Use Streamlit secrets for credentials
            user=st.secrets.mysql.user,
            password=st.secrets.mysql.password,  # ✅ Secure credentials
            database=st.secrets.mysql.database,
        )
        cursor = conn.cursor(dictionary=True)  # Fetch results as dictionary

        cursor.execute("SELECT * FROM UserDetails")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows if rows else None
    except mysql.connector.Error as e:
        print(f"❌ MySQL Error: {e}")
        return None


def check_face_data():
    """Checks if the given name and email have a matching Face ID."""
    name, email = load_list_json()
    if not name or not email:
        logger.info("No name and email found in list.json.")
        return None, "No name and email found in list.json."

    database_faces = fetch_database_data()
    if not database_faces:
        return None, "No data found in the database."

    for row in database_faces:
        logger.info(f"Database Row: {row}")  # Debugging statement
        print("Database Row:", row)  # Debugging statement

        # Ensure case-insensitive matching for name and email
        if (
            row.get("NAME", "").lower() == name.lower()
            and row.get("MAIL_ID", "").lower() == email.lower()
        ):
            face_id = row.get("SERVER_ID", "No Face ID")  # Check if face_id exists

            # If face_id is "No Face ID", return an error message
            if face_id == "No Face ID":
                return None, "⚠️ Face is not added by the system."

            return {
                "name": row["NAME"],
                "email": row["MAIL_ID"],
                "image_url": row.get("IMAGE_URL", None),  # Image URL if available
            }, None

    return None, "No matching Face ID found."
