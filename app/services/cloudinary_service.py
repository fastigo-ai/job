import cloudinary
import cloudinary.utils
import cloudinary.uploader
from app.config import (
    CLOUDINARY_CLOUD_NAME,
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET
)

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)


def upload_image(file):
    result = cloudinary.uploader.upload(file)
    return result["secure_url"]
def upload_resume(file):
    result = cloudinary.uploader.upload(
        file,
        resource_type="raw",     # IMPORTANT
        folder="job_resumes",
        # format="pdf"
    )
    return {
        "url": result["secure_url"],
        "public_id": result["public_id"]
    }
def get_downloadable_resume_url(public_id):
    url, _ = cloudinary.utils.cloudinary_url(
        public_id,
        resource_type="raw",
        flags="attachment"
    )
    return url