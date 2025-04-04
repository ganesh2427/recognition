import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.module.recognizeface import load_json_data, recognize


def main():
    data = load_json_data()
    if data:
        recognition_results = recognize(data)

        if recognition_results:
            print("\n🎯 Recognition Summary:")
            for res in recognition_results:
                print(
                    f"🔹 Name: {res['name']}, Email: {res['email']}, Face ID: {res['face_id']}"
                )
                print(f"📷 Uploaded Image: {res['uploaded_image']}")
                print(f"📷 Matched Image: {res['matched_image']}")
        else:
            print("⚠️ No faces recognized.")


if __name__ == "__main__":
    main()
