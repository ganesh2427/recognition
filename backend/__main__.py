import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.module.face_recognition import app


def main():
    app()


if __name__ == "__main__":
    main()
