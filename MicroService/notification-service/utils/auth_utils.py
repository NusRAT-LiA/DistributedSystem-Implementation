import requests
from fastapi import HTTPException, Depends, status
from models import User

AUTH_SERVICE_URL = "http://localhost:8000/auth/me"  # Change to actual URL of the auth service

def getCurrentUser(token) -> User:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(AUTH_SERVICE_URL, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return User(**user_data)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
