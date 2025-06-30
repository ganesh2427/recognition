# Recognition: Face Recognition System

## Project Description
This project is a face verification system that uses the Eden AI API to compare facial images and determine if they belong to the same person. Users can register, list, delete, and verify faces using static image inputs, with local image storage and optional AWS S3 integration for remote backups. Instead of running face recognition locally, the system offloads the comparison task to Eden AI’s cloud-based API, enabling accurate and scalable verification without the need for a heavy deep learning model on-device. 
The codebase is modular and includes separate scripts for each operation, along with structured logging for monitoring and debugging. While the system currently works with uploaded images, it is flexible and can be extended to support real-time webcam-based input if needed. This makes it suitable for lightweight deployments in secure authentication, user onboarding, or ID verification systems. The design prioritizes clarity, modularity, and cloud compatibility for real-world use.
## Table Of Contents

## Features

- **Face Detection and Recognition**: Detects faces in images and matches them against a database of known faces.
- **AWS S3 Integration**: Stores and retrieves images from an S3 bucket.
- **MySQL Database**: Manages face data and metadata.
- **Streamlit Interface**: Provides a user-friendly web interface for interacting with the system.
- **Environment Configuration**: Uses `.env` for managing sensitive credentials.

## Requirements

- Python >= 3.12
- MySQL Server
- AWS S3 Bucket
- EdenAI API Key (for additional AI services)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/recognition.git
   cd recognition

2. Install dependencies using Poetry:
    ```bash
    poetry install

3. Set up the .env file with your credentials:
   ```bash
   # MySQL Database Credentials
    MYSQL_HOST=127.0.0.1
    MYSQL_USER=root
    MYSQL_PASSWORD=your_password
    MYSQL_DATABASE=your_database

    # AWS Credentials
    AWS_ACCESS_KEY=your_aws_access_key
    AWS_SECRET_KEY=your_aws_secret_key
    AWS_BUCKET_NAME=your_bucket_name
    AWS_REGION=your_region

    # EdenAI API Key
    EDENAI_API_KEY=your_edenai_api_key


## How To Run

1. Run the backend module:
   ```bash
   poetry run streamlit run backend/__main__.py 