import json
import streamlit as st
import mysql.connector
import requests
import os
from dotenv import load_dotenv  

load_dotenv()

JSON_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)),"module","jsons", "recognizeface.json")

# ✅ Get credentials from environment variables
MYSQL_HOST = st.secrets.mysql.host
MYSQL_USER = st.secrets.mysql.user
MYSQL_PASSWORD = st.secrets.mysql.password
MYSQL_DATABASE = st.secrets.mysql.database
EDENAI_API_KEY = st.secrets.edenai.api_key  # Secure API key


# ✅ Save recognition input data to JSON file
def save_recognize_json(name, email, image_url):
    """Save recognition input data to JSON file."""
    data = {"user_info": [{"name": name, "mail_id": email, "image_url": image_url}]}
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ✅ Load recognition input data from JSON file
def load_json_data():
    """Load recognition input data from JSON file."""
    try:
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error loading JSON: {e}")
        return None


# ✅ Function to send image to API and recognize face
def recognizeface(file_url):
    url = "https://api.edenai.run/v2/image/face_recognition/recognize"

    payload = {
        "response_as_dict": True,
        "attributes_as_list": False,
        "show_original_response": False,
        "providers": "amazon",
        "file_url": file_url,
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {EDENAI_API_KEY}",  # ✅ Secure API key
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.ok:
        try:
            items = response.json().get("amazon", {}).get("items", [])
            return items[0]["face_id"] if items else None
        except (KeyError, IndexError):
            return None
    return None


# ✅ Connect to the MySQL database
def connect_db():
    """Connect to MySQL securely."""
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
        )
        if conn.is_connected():
            print("✅ Connected to MySQL")
            return conn
    except mysql.connector.Error as e:
        print("❌ Database Connection Error:", e)
        return None


# ✅ Recognize faces and fetch user details
def recognize(data):
    """Match faces in database."""
    if not data:
        print("⚠️ No data found in JSON file.")
        return None

    conn = connect_db()
    if not conn:
        return None

    cur = conn.cursor()
    results = []

    for item in data.get("user_info", []):
        image_url = item.get("image_url")
        mail_id = item.get("mail_id")

        if not image_url or not mail_id:
            print("⚠️ Skipping entry due to missing data:", item)
            continue

        face_id = recognizeface(image_url)

        if face_id:
            print(f"✅ Face ID Recognized: {face_id}")

            try:
                sql_select = "SELECT MAIL_ID, NAME, IMAGE_URL FROM UserDetails WHERE SERVER_ID = %s"
                cur.execute(sql_select, (face_id,))
                result = cur.fetchone()

                if result:
                    recognized_mail, recognized_name, recognized_image = result
                    print(f"🔹 Recognized: {recognized_name}, Email: {recognized_mail}")

                    results.append(
                        {
                            "name": recognized_name,
                            "email": recognized_mail,
                            "uploaded_image": image_url,
                            "matched_image": recognized_image,
                            "face_id": face_id,
                        }
                    )
                else:
                    print("❌ No match found in the database.")

                cur.fetchall()  # ✅ Prevent "Unread result" MySQL error

            except mysql.connector.Error as e:
                print("❌ SQL Error:", e)
        else:
            print("❌ No face match found for image:", image_url)

    conn.commit()
    cur.close()
    conn.close()

    return results


# ✅ Run recognition process
if __name__ == "__main__":
    data = load_json_data()
    if data:
        recognition_results = recognize(data)

        if recognition_results:
            print("\n🎯 Recognition Summary:")
            for res in recognition_results:
                print(f"🔹 Name: {res['name']}, Email: {res['email']}, Face ID: {res['face_id']}")
                print(f"📷 Uploaded Image: {res['uploaded_image']}")
                print(f"📷 Matched Image: {res['matched_image']}")
        else:
            print("⚠️ No faces recognized.")

