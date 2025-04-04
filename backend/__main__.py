import sys
import os
import streamlit as st

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.module import face_recognition

def main():
    st.title("Face Recognition App")
    st.write("Click the button below to run face recognition.")
    
    if st.button("Run Face Recognition"):
        face_recognition()
        st.success("Face recognition completed!")

# To run the app, use the following command in the terminal:
# streamlit run /Users/gk/Documents/GitHub/Face/backend/__main__.py

if __name__ == "__main__":
    main()