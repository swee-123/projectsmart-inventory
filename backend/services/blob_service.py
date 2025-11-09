import os
from azure.storage.blob import BlobServiceClient
from fastapi import UploadFile
import uuid

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

if not connection_string:
    raise Exception("AZURE_STORAGE_CONNECTION_STRING is missing.")

blob_service = BlobServiceClient.from_connection_string(connection_string)


def upload_file_to_container(container_name: str, file: UploadFile):
    unique_name = f"{uuid.uuid4()}-{file.filename}"
    blob_client = blob_service.get_blob_client(container=container_name, blob=unique_name)

    blob_client.upload_blob(file.file, overwrite=True)

    return blob_client.url

def upload_local_file(container_name: str, file_path: str):
    blob_name = os.path.basename(file_path)
    blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    return blob_client.url

