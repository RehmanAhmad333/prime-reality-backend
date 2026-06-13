# This module defines the S3Service class, which provides functionality to upload images to an AWS S3 bucket. It uses the boto3 library to interact with AWS S3 and includes error handling for potential issues during the upload process. The `upload_image_to_s3` function takes an uploaded file and an optional folder name, generates a unique filename, and uploads the file to the specified S3 bucket. It returns the public URL of the uploaded image, assuming the bucket is configured for public read access. If the upload fails, it raises an exception with details about the failure.

import boto3
import uuid
from botocore.exceptions import ClientError
from fastapi import UploadFile
from app.core.config import settings


s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

def upload_image_to_s3(file: UploadFile, folder: str = "properties") -> str:
    """Uploads an image to S3 and returns the public URL."""
    try:
        # Generate unique filename
        ext = file.filename.split('.')[-1]
        key = f"{folder}/{uuid.uuid4()}.{ext}"
        
        # Upload
        s3_client.upload_fileobj(
            file.file,
            settings.AWS_S3_BUCKET,
            key,
            ExtraArgs={'ContentType': file.content_type}
        )
        
        # Construct public URL (assuming bucket is public-read)
        url = f"https://{settings.AWS_S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"
        return url
    except ClientError as e:
        raise Exception(f"S3 upload failed: {e}")