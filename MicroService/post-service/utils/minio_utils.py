from minio import Minio, S3Error
from config import settings

minioClient = Minio(
    settings.minioEndpoint,
    access_key=settings.minioAccessKey,
    secret_key=settings.minioSecretKey,
    secure=False
)

if not minioClient.bucket_exists("snippets"):
    minioClient.make_bucket("snippets")

def uploadCodeSnippet(fileData, fileName):
    minioClient.put_object(
        "snippets", fileName, fileData, length=-1, part_size=10*1024*1024
    )

def getCodeSnippet(postId):
    try:
        objects = minioClient.list_objects("snippets", prefix=f"{postId}_")
        obj = next(objects, None)  
        
        if obj is not None:
            response = minioClient.get_object("snippets", obj.object_name)
            
            content = response.read()  
            
            
            return content  
        else:
            return None  
    except S3Error as e:
        print(f"error retrieving file: {e}")
        return None