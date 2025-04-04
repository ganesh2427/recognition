
import json
import mysql.connector
import requests
import os
from dotenv import load_dotenv  # ✅ Load environment variables

# ✅ Load environment variables from .env file
load_dotenv()

JSON_FILE = os.path.join(os.path.dirname(__file__), "input.json")

def save_json(name, email, image_url):
    """Overwrites the JSON file with the latest details only."""
    data = {
        "user_info": [
            {
                "name": name,
                "mail_id": email,
                "image_url": image_url
            }
        ]
    }
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

def addface(file_url):
    url = "https://api.edenai.run/v2/image/face_recognition/add_face"

    payload = {
        "response_as_dict": True,
        "attributes_as_list": False,
        "show_original_response": False,
        "providers": "amazon",
        "file_url": file_url
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {os.getenv('EDENAI_API_KEY')}"  # ✅ API Key from .env
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()   
        return response.json()  # ✅ Return JSON instead of text
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return None  # Return None if request fails

# ✅ Load User Data from input.json
try:
    with open(JSON_FILE, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("❌ Error: input.json file not found!")
    exit()

# ✅ Function to Insert Data into MySQL
def insert_data(data):
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),  # ✅ Secure credentials
            database=os.getenv("MYSQL_DATABASE")
        )
        if conn.is_connected():
            print("✅ Connected to MySQL database")
    except mysql.connector.Error as e:
        print(f"❌ MySQL Connection Error: {e}")
        return

    cur = conn.cursor()

    for item in data.get("user_info", []):
        mail_id = item.get("mail_id")
        name = item.get("name")
        image_url = item.get("image_url")

        # ✅ Call API to get face ID
        response = addface(image_url)
        if response is None:
            print(f"⚠️ Skipping {mail_id} due to API error")
            continue

        # ✅ Extract Face IDs
        face_ids = response.get("amazon", {}).get("face_ids", [])
        face_id = ", ".join(face_ids) if face_ids else "No Face ID"
        print(f"👤 Face ID for {mail_id}: {face_id}")

        # ✅ Insert into MySQL
        try:
            sql_insert = "INSERT INTO UserDetails (MAIL_ID, NAME, IMAGE_URL, SERVER_ID) VALUES (%s, %s, %s, %s)"
            cur.execute(sql_insert, (mail_id, name, image_url, face_id))
            print(f"✅ Inserted: {mail_id} | {name} | {face_id}")
        except mysql.connector.IntegrityError:
            print(f"⚠️ Duplicate entry for {mail_id}, Skipping...")
            continue

    # ✅ Commit and close connection
    conn.commit()
    cur.close()
    conn.close()
    print("🎉 All data processed successfully!")

# ✅ Run the function
insert_data(data)
