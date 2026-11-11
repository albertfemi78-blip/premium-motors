import os
import requests
import cloudinary
import cloudinary.uploader

from django.core.files.storage import Storage
from django.core.files.base import ContentFile

class CloudinaryMediaStorage(Storage):


def _save(self, name, content):
    public_id = os.path.splitext(name)[0]

    cloudinary.uploader.upload(
        content,
        public_id=public_id,
        overwrite=True,
        resource_type="image"
    )

    return name

def _open(self, name, mode="rb"):
    public_id = os.path.splitext(name)[0]
    image_format = os.path.splitext(name)[1].lstrip(".")

    url = cloudinary.CloudinaryImage(public_id).build_url(
        secure=True,
        format=image_format
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    return ContentFile(response.content)

def exists(self, name):
    return False

def url(self, name):
    public_id = os.path.splitext(name)[0]
    image_format = os.path.splitext(name)[1].lstrip(".")

    return cloudinary.CloudinaryImage(public_id).build_url(
        secure=True,
        format=image_format
    )

def delete(self, name):
    public_id = os.path.splitext(name)[0]

    cloudinary.uploader.destroy(
        public_id,
        resource_type="image"
    )

