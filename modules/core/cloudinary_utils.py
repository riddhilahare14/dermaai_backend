# modules/core/cloudinary_utils.py
import os
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile

cloudinary.config(
  cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", ""),
  api_key=os.getenv("CLOUDINARY_API_KEY", ""),
  api_secret=os.getenv("CLOUDINARY_API_SECRET", ""),
  secure=True
)

def upload_file_to_cloudinary(upload_file: UploadFile) -> str:
    """
    upload_file_to_cloudinary: Uploads an UploadFile to Cloudinary and returns the URL.
    If Cloudinary vars are not set, you may want to save locally instead.
    """
    contents = upload_file.file.read()
    result = cloudinary.uploader.upload(contents, folder="dermaai_images")
    return result.get("secure_url")
