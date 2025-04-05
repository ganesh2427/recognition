import sys
import os
from pathlib import Path

# Add the project root directory to sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Now we can import from backend module
from backend.module.face_recognition import app


def main():
    app()


if __name__ == "__main__":
    main()