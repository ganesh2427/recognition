import logging

def get_logger():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("face_recognition.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)
