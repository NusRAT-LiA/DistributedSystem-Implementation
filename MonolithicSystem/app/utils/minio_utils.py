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
        # Retrieve the first object in the 'snippets' bucket that starts with the post ID
        objects = minioClient.list_objects("snippets", prefix=f"{postId}_")
        obj = next(objects, None)  # Get the first object or None if no object is found
        
        if obj is not None:
            # Get the object content
            response = minioClient.get_object("snippets", obj.object_name)
            
            # Read the object content
            content = response.read()  # Reads the file content
            
            # Optionally, decode the content if it's text (e.g., UTF-8)
            # content = content.decode('utf-8')  # Uncomment if you want a string
            
            return content  # Return the raw content as bytes (or as a string if decoded)
        else:
            return None  # If no object is found
    except S3Error as e:
        print(f"Error retrieving file: {e}")
        return None