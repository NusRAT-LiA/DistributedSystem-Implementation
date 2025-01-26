import requests

# Step 1: Sign in and get the token
signin_url = "http://localhost:8000//auth/signin"
signin_payload = {"email": "string22", "password": "string2"}
response = requests.post(signin_url, json=signin_payload)

if response.status_code == 200:
    token = response.json().get("accessToken")
    headers = {"Authorization": f"Bearer {token}"}

    # Step 2: Use the token to access protected endpoints
    me_url = "http://localhost:8000//auth/me"
    me_response = requests.get(me_url, headers=headers)

    if me_response.status_code == 200:
        print(me_response.json())  # Display the current user's information
    else:
        print(f"Error: {me_response.status_code}, {me_response.json()}")
else:
    print(f"Sign-in failed: {response.status_code}, {response.json()}")
