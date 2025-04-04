import streamlit as st
import os
import json
from backend.module.s3bucket import upload_to_s3  # Importing the upload function
from backend.module.addface_ import (
    insert_data,
    save_json,
)  # Importing function from addface.py
from backend.module.listface import check_face_data, load_list_json, save_list_json
import pandas as pd
from backend.module.deleteface import delete_data
from backend.module.recognizeface import save_recognize_json, load_json_data, recognize


JSON_FILE = os.path.join(os.path.dirname(__file__), "jsons", "input.json")
LIST_JSON_FILE = os.path.join(os.path.dirname(__file__), "jsons", "list.json")


def app():
     
    st.title("Face Recognition System")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["➕ Add Face", "📋 List Faces", "🔍 Recognize Face", "🗑️ Delete Face"]
    )

    with tab1:
        st.header("Add a New Face")
        name = st.text_input("Enter Name", key="add_name_key")
        email = st.text_input("Enter Email ID", key="add_email_key")
        image = st.file_uploader(
            "Upload Face Image", type=["jpg", "jpeg", "png"], key="add_image_key"
        )

        if st.button("Save Face", key="save_face_key"):
            if image and email:
                file_path = f"temp_{image.name}"
                with open(file_path, "wb") as f:
                    f.write(image.getbuffer())

                # Upload to S3 using email as the filenames
                image_url = upload_to_s3(file_path, email)

                # Remove local temp file
                os.remove(file_path)

                if image_url:
                    # Overwrite JSON file with latest details
                    save_json(name, email, image_url)

                    # ✅ Call insert_data() directly from addface.py
                    with open(JSON_FILE, "r") as file:
                        data = json.load(file)
                    insert_data(
                        data
                    )  # Call function to process face & insert into MySQL

                    st.success(f"✅ Face for {name} has been added successfully!")
                    st.write(f"📧 Email: {email}")
                    st.image(image_url, caption="Uploaded Image", use_column_width=True)
                else:
                    st.error("❌ Failed to upload image.")
            else:
                st.warning("⚠️ Please provide an email and upload an image.")

    with tab2:
        st.header("Enter Name and Email")
        name = st.text_input("Enter Name", key="list_name_key")
        email = st.text_input("Enter Email ID", key="list_email_key")

        if st.button("Save Details", key="save_list_key"):
            if name and email:
                save_list_json(name, email)
                st.success(f"✅ Details for {name} have been saved successfully!")
                st.write(f"📧 Email: {email}")
            else:
                st.warning("⚠️ Please enter both name and email.")

        # Check for matching Face ID after saving
        st.header("Check Face Data from List")

        # Load user details from list.json
        saved_name, saved_email = load_list_json()

        if saved_name and saved_email:
            st.write(f"**📌 Name:** {saved_name}")
            st.write(f"**📧 Email:** {saved_email}")

            # Check for matching face data
            face_data, error_message = check_face_data()

            if face_data:
                st.success("✅ Face ID found!")

                # Format data for tabular display
                df = pd.DataFrame(
                    [
                        {
                            "Name": face_data["name"],
                            "Email": face_data["email"],
                            "Image URL": face_data["image_url"],
                        }
                    ]
                )
                st.table(df)

                # Show image if Face ID exists
                if face_data["image_url"]:
                    st.image(
                        face_data["image_url"],
                        caption="Face Image",
                        use_column_width=True,
                    )
            else:
                st.warning(f"⚠️ {error_message}")
        else:
            st.warning("⚠️ No name and email found in list.json.")

    with tab3:
        st.header("Recognize a Face")

        recognize_name = st.text_input("Enter Name", key="recognize_name_key")
        recognize_email = st.text_input("Enter Email ID", key="recognize_email_key")
        recognize_image = st.file_uploader(
            "Upload Face Image", type=["jpg", "jpeg", "png"], key="recognize_image_key"
        )

        if st.button("Recognize Face", key="recognize_face_key"):
            if recognize_image and recognize_email:
                file_path = f"temp_{recognize_image.name}"
                with open(file_path, "wb") as f:
                    f.write(recognize_image.getbuffer())

                # Convert image to HTTPS link by uploading to S3
                image_url = upload_to_s3(file_path, recognize_email)

                # Remove local temp file
                os.remove(file_path)

                if image_url:
                    # ✅ Save data to JSON before calling recognize function
                    save_recognize_json(recognize_name, recognize_email, image_url)

                    # ✅ Load JSON data
                    data = load_json_data()

                    if data:
                        # ✅ Call recognize() with the loaded data and store results
                        recognition_results = recognize(data)

                        if recognition_results:
                            st.success("✅ Face recognition successful!")

                            for res in recognition_results:
                                st.subheader("🔹 Recognized Details:")
                                st.write(f"**Name:** {res['name']}")
                                st.write(f"**Email:** {res['email']}")
                                st.write(f"**Face ID:** {res['face_id']}")

                                # Display both uploaded and matched images
                                st.image(
                                    res["uploaded_image"],
                                    caption="📷 Uploaded Image",
                                    use_column_width=True,
                                )
                                st.image(
                                    res["matched_image"],
                                    caption="📷 Matched Image",
                                    use_column_width=True,
                                )

                        else:
                            st.warning("⚠️ No matching face found in the database.")

                    else:
                        st.error("❌ Failed to load JSON data.")

                else:
                    st.error("❌ Failed to upload image.")
            else:
                st.warning("⚠️ Please provide an email and upload an image.")

    with tab4:
        st.header("Delete a Face Record")
        delete_name = st.text_input("Enter Name", key="delete_name_key")
        delete_email = st.text_input("Enter Email ID", key="delete_email_key")

        if st.button("Delete Face", key="delete_face_key"):
            if delete_email:
                success, message = delete_data(delete_email)

                if success:
                    st.success(message)
                else:
                    st.warning(message)
            else:
                st.warning("⚠️ Please enter the email ID to delete the record.")


if __name__ == "__main__":
    app()
