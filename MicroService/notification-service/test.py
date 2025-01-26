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
    url = f"http://localhost:8002/notification/?token={token}"
    payload = {
    "postId": 3,  
    "message": "This is a test notification"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
     print("Notification created successfully:", response.json())
    else:
     print(f"Error: {response.status_code}, {response.json()}")

    response2 = requests.get(url, headers=headers)
    print(response2.json())

    if response2.status_code == 200:
      print("Notifications fetched successfully:", response2.json())
    else:
      print(f"Error: {response2.status_code}, {response2.json()}")

    notification_id = 2   

    puturl = f"http://localhost:8002/notification/{notification_id}/mark_seen" 
    response3 = requests.put(puturl, headers=headers)
    if response3.status_code == 200:
     print(response3.json())
    else:
     print(f"Error: {response3.status_code}, {response3.json()}")



else:
    print(f"Sign-in failed: {response.status_code}, {response.json()}")
