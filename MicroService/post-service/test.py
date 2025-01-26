import requests
import os


# Step 1: Sign in to Auth Service
signin_url = "http://localhost:8000//auth/signin"
signin_payload = {"email": "string22", "password": "string2"}
response = requests.post(signin_url, json=signin_payload)

if response.status_code == 200:
    token = response.json().get("accessToken")
    headers = {"Authorization": f"Bearer {token}"}

    # Step 2: Create a post with a file upload
    post_url = f"http://localhost:8001/post/?token={token}"
    post_payload = {"content": "This is a test post"}
    # test_file_path = "test_file.py"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_file_path = os.path.join(script_dir, "test_file.py")

    with open(test_file_path, "rb") as file:
        files = {"codeFile": file}
        post_response = requests.post(post_url, data=post_payload, files=files, headers=headers)

    if post_response.status_code == 200:
        print(post_response.json())  # Confirm upload was successful
    else:
        print(f"Error: {post_response.status_code}, {post_response.json()}")
    
    # get_response=requests.get(post_url,headers=headers)
    # print(get_response.json())

else:
    print(f"Sign-in failed: {response.status_code}, {response.json()}")
