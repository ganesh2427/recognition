# Recognition: Face Recognition System













## Project Description
This project is a face verification system that uses the Eden AI API to compare facial images and determine if they belong to the same person. Users can register, list, delete, and verify faces using static image inputs, with local image storage and optional AWS S3 integration for remote backups. Instead of running face recognition locally, the system offloads the comparison task to Eden AI’s cloud-based API, enabling accurate and scalable verification without the need for a heavy deep learning model on-device. 

The codebase is modular and includes separate scripts for each operation, along with structured logging for monitoring and debugging. While the system currently works with uploaded images, it is flexible and can be extended to support real-time webcam-based input if needed. This makes it suitable for lightweight deployments in secure authentication, user onboarding, or ID verification systems. The design prioritizes clarity, modularity, and cloud compatibility for real-world use.











## Table Of Contents

- [Background](#Background)
    - [Context and Motivation](#context-and-motivation)
    - [Objectives](#objectives)
    - [Significance of the Project](#significance-of-the-Project)
- [System Functionality Overview](#System-Functionality-Overview)
    - [Add Face](#Add-Face)
    - [List Face](#List-Face)
    - [Recognize-Face](#Recognize-Face)
    - [Delete Face](#Delete-Face)
- [Technologies Used](#Technologies-Used)
    - [Core-Technologies](#Core-Technologies)
    - [Cloud Services & APIs](#Cloud-Services-&-APIs)
    - [Data Management](#Data-Management)
    - [Dependency & Configuration Management](#Dependency-&-Configuration-Management)
    - [External Communication](#External-Communication)
- [Installation](#Installation)
    - [Prerequisites](#Prerequisites)
    - [Steps](#Steps)
- [Project Structure](#Project-Structure)












## Background

This project implements a modular face verification system that utilizes Eden AI’s cloud-based face recognition API to compare and verify facial identities. It allows users to register, list, delete, and verify faces using static images, eliminating the need for real-time webcam input or locally hosted deep learning models. Optional integration with AWS S3 enables remote storage and backup of face data. The system leverages cloud intelligence for accurate verification, providing a lightweight, scalable solution suitable for various authentication and security applications.

### Context and Motivation

With the rapid growth of digital identity systems, face recognition has become a cornerstone in biometric authentication — from online onboarding and secure access control to surveillance and law enforcement. However, deploying accurate and efficient facial recognition solutions often requires high computational resources and complex infrastructure, which may not be practical for lightweight systems or developers lacking deep learning expertise. Traditional on-device recognition models can also face challenges related to scalability, maintenance, and performance in real-world scenarios.

To address these limitations, this project adopts a cloud-first approach by integrating with Eden AI’s face recognition API. This eliminates the burden of model training, infrastructure scaling, and version control — making advanced face verification accessible, fast, and easily deployable.

### Objectives

This project aims to build a user-friendly, API-driven face verification system with the following goals:

Cloud-based Recognition: Integrate Eden AI's face recognition API to compare image pairs and provide match results using similarity scores.

Modular Design: Develop clear and independent scripts for face registration, listing, deletion, and verification.

Cloud Storage: Allow optional uploading of face data to AWS S3 for backup, remote access, or distributed use.

Static Image Input: Operate on uploaded image files (not real-time webcam) for more control and reproducibility.

Extensibility: Maintain code flexibility to easily support future features like real-time webcam input or alternative APIs.

### Significance of the Project

This project demonstrates that robust face verification can be achieved without relying on heavy local models by offloading the intelligence to reliable cloud services like Eden AI. The system offers a practical, resource-efficient alternative to conventional deep learning deployments, making it suitable for developers, startups, and organizations seeking to integrate biometric features without investing in complex infrastructure. Its clean modular structure encourages reuse and adaptation for different applications such as secure onboarding, user verification, or automated ID validation. Furthermore, with optional AWS S3 support, it showcases a hybrid design combining cloud computation and cloud storage — laying the groundwork for future extensions such as multi-user web apps or real-time monitoring interfaces.










## System Functionality Overview

The face verification system deployed through this application is designed to support four essential operations: Add Face, List Face, Recognize Face, and Delete Face. Each operation is seamlessly integrated with a cloud-based backend using the Eden AI Face Recognition API, and all user data is securely managed through a database where each entry is uniquely identified using a generated face_id.

### 1. Add Face
This operation allows users to register their identity into the system by providing the following details:

      Name

      Email ID (used as the primary key)

      Facial Image

Once submitted:

   - The image is uploaded and processed through the Eden AI API.

   - A unique face_id is generated by the API for the user's facial features.

   - This face_id, along with the user's name, email, and image metadata, is stored in the system database.

   - This feature lays the foundation for future verification by ensuring each registered face is uniquely identifiable.

### 2. List Face
This feature retrieves the stored image and metadata for any registered user. The user needs to provide:

      Name

      Email ID

The system will:

   - Search the database for the provided email ID.

   - If a match is found, the system displays the user’s previously uploaded facial image and stored details.

   - This feature is useful for reviewing enrolled identities.

### 3. Recognize Face
This feature verifies whether an uploaded face matches a previously registered identity. To perform recognition, the user must submit:

      Name

      Email ID

      Facial Image (to be verified)

Internally, the system:

   - Fetches the stored face_id associated with the provided email.

   - Sends both the stored face and the newly uploaded face to the Eden AI API.

   - The API performs face comparison and returns whether the two images match, along with a similarity score.

   - This task is core to the face verification system and enables reliable identity authentication.

### 4. Delete Face
This operation removes a user’s facial data from the system. The user must provide:

      Name

      Email ID

Upon submission:

   - The system identifies the user via the email ID.

   - All associated data (face ID, image, and metadata) is permanently deleted from the database.

   - This ensures users have control over their data and supports privacy compliance.


WorkFlow:

<p align="center">
  <img src="image/workflow image.png" alt="Relative Path" width="600"/>
</p>









## Technologies Used

This face recognition project leverages a combination of modern tools and frameworks to ensure scalability, security, and performance:

### Core Technologies

- Python 3.12+
Primary programming language for backend logic and system integration.

- Streamlit
Lightweight and interactive framework for building web-based user interfaces in Python.

### Cloud Services & APIs

- Eden AI API
Used for cloud-based face verification and comparison, enabling off-device processing for improved performance and scalability.

- AWS S3 (Amazon Simple Storage Service)
Cloud storage solution for securely storing and retrieving facial images.

### Data Management

- MySQL
Relational database system for storing user profiles, face IDs, and associated metadata.

- Pandas
Powerful data analysis and manipulation library used for managing tabular data formats.

### Dependency & Configuration Management

- Poetry
Modern Python dependency management and packaging tool for streamlined project setup and version control.

- python-dotenv
For loading environment variables securely from .env files, managing sensitive credentials and configuration settings.

### External Communication

- Requests
HTTP library for making API calls to services like Eden AI.

- boto3
AWS SDK for Python to interact with AWS S3 and manage cloud resources programmatically.

- mysql-connector-python
Official MySQL connector for Python, facilitating secure and efficient database interaction.










## Installation

### Prerequisites

- **Python 3.12+**: [Download Python](https://www.python.org/downloads/)
- **pip**: Comes with Python, but ensure it's up to date  
  ```bash
  python -m pip install --upgrade pip
  ```
- **Git**: For cloning the repository ([Download Git](https://git-scm.com/downloads))
- **Poetry**: For dependency management  
  ```bash
  pip install poetry
  ```
- **MySQL Server**: For database storage ([Download MySQL](https://dev.mysql.com/downloads/mysql/))
- **AWS Account**: For S3 bucket usage ([AWS S3](https://aws.amazon.com/s3/))
- **EdenAI API Key**: [Get API Key](https://app.edenai.run/admin/account)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/recognition.git
   cd recognition
   ```

2. **(Optional) Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

4. **Set up the `.env` file with your credentials:**
   ```properties
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
   ```

5. **Run the backend module:**
   ```bash
   poetry run streamlit run backend/__main__.py
   ```

---

**Note:**  
All required Python packages (such as `boto3`, `mysql-connector-python`, `pandas`, `python-dotenv`, `requests`, `streamlit`) are managed by Poetry and specified in `pyproject.toml`.  
If you encounter issues with Poetry, you can also install dependencies directly with pip using a `requirements.txt` generated by Poetry:

```bash
poetry export -f requirements.txt --output requirements.txt
pip install -r requirements.txt
```


## Project Structure



The repository is organized as follows:

```
.
├── README.md
├── backend
│   ├── __init__.py
│   ├── __main__.py
│   └── module
│       ├── __init__.py
│       ├── addface_.py
│       ├── deleteface.py
│       ├── face_recognition.py
│       ├── jsons
│       │   ├── input.json
│       │   ├── list.json
│       │   └── recognizeface.json
│       ├── listface.py
│       ├── logger.py
│       ├── recognizeface.py
│       ├── s3bucket.py
│       └── test.py
├── face_recognition.log
├── poetry.lock
├── pyproject.toml
└── requirements.txt
```