from minio import Minio
from fastapi import UploadFile

minio_client = Minio(
    "192.168.0.117:9000",  
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=True
)

def upload_file_to_minio(file: UploadFile):
    bucket_name = "posts"
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    file_name = file.filename
    file_content = file.file.read()

    minio_client.put_object(
        bucket_name=bucket_name,
        object_name=file_name,
        data=file.file,
        length=len(file_content),
        content_type=file.content_type,
    )

    return f"http://{minio_client._endpoint}/{bucket_name}/{file_name}"
