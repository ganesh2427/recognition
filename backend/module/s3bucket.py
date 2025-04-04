import boto3
import os
import mimetypes
import re  # For cleaning file names
from dotenv import load_dotenv

load_dotenv()


# Get AWS credentials from environment variables
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")


def clean_file_name(file_name):
    """Cleans file names to be S3-compatible."""
    file_name = file_name.replace(" ", "_")  # Replace spaces with underscores
    file_name = re.sub(
        r"\.+", ".", file_name
    )  # Replace multiple dots with a single dot
    file_name = re.sub(r"[^a-zA-Z0-9._-]", "", file_name)  # Remove invalid characters
    return file_name


def upload_to_s3(file_path, email):
    """Uploads a file to S3 using email as the file name and returns its public URL."""
    try:
        s3 = boto3.client(
            "s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY
        )

        ext = os.path.splitext(file_path)[-1]
        safe_email = clean_file_name(email.split("@")[0])
        file_name = f"{safe_email}{ext}"

        content_type, _ = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = "application/octet-stream"

        s3.upload_file(
            file_path,
            AWS_BUCKET_NAME,
            file_name,
            ExtraArgs={"ContentType": content_type},
        )

        file_url = (
            f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_name}"
        )
        return file_url

    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None
