from minio import Minio
from config import settings

minioClient = Minio(
    settings.minioEndpoint,
    access_key=settings.minioAccessKey,
    secret_key=settings.minioSecretKey,
    secure=False
)

# Ensure the bucket exists
if not minioClient.bucket_exists("snippets"):
    minioClient.make_bucket("snippets")

def uploadCodeSnippet(fileData, fileName):
    minioClient.put_object(
        "snippets", fileName, fileData, length=-1, part_size=10*1024*1024
    )
