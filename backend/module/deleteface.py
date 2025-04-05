import json
import mysql.connector
import requests
import os
from dotenv import load_dotenv  # ✅ Load environment variables
import streamlit as st  # ✅ Streamlit for web app
# ✅ Load environment variables from .env file
load_dotenv()


# Function to delete face from the API
def deleteface(face_id):
    url = "https://api.edenai.run/v2/image/face_recognition/delete_face"

    payload = {
        "response_as_dict": True,
        "attributes_as_list": False,
        "show_original_response": False,
        "providers": "amazon",
        "face_id": face_id,
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {st.secrets.edenai.api_key}",  # ✅ API Key from .env
    }

    response = requests.post(url, json=payload, headers=headers)

    # Handle API response
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get("amazon", {}).get("status") == "success":
            return True, "✅ Face successfully deleted from API."
        else:
            return False, "⚠️ Face not found in API, but will delete from database."
    else:
        return False, f"❌ API Error: {response.text}"


# Function to delete user data
def delete_data(email):
    if not email:
        return False, "❌ Error: Email cannot be empty!"

    # Connect to MySQL database
    try:
        conn = mysql.connector.connect(
            host=st.secrets.mysql.host,  # ✅ Use Streamlit secrets for credentials
            user=st.secrets.mysql.user,
            password=st.secrets.mysql.password,  # ✅ Secure credentials
            database=st.secrets.mysql.database,
        )
        if not conn.is_connected():
            return False, "❌ Error: Unable to connect to MySQL database."
    except Exception as e:
        return False, f"❌ Database connection error: {str(e)}"

    cur = conn.cursor()

    try:
        # Step 1: Fetch Face ID from database
        sql_select = "SELECT SERVER_ID FROM UserDetails WHERE MAIL_ID = %s"
        cur.execute(sql_select, (email,))
        face_id_result = cur.fetchone()

        if not face_id_result:
            # If no Face ID is found, delete the user from the database
            sql_delete = "DELETE FROM UserDetails WHERE MAIL_ID = %s"
            cur.execute(sql_delete, (email,))
            conn.commit()
            cur.close()
            conn.close()
            return True, f"⚠️ No Face ID found, but user {email} was deleted from DB."

        face_id = face_id_result[0]

        # Step 2: Call API to delete face
        api_success, api_message = deleteface(face_id)

        # Step 3: Always delete from database
        sql_delete = "DELETE FROM UserDetails WHERE MAIL_ID = %s"
        cur.execute(sql_delete, (email,))
        conn.commit()

        cur.close()
        conn.close()

        return True, f"{api_message} ✅ User {email} deleted from DB."

    except mysql.connector.Error as e:
        return False, f"❌ MySQL Error: {str(e)}"
