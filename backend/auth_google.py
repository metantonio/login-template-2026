from google.oauth2 import id_token
from google.auth.transport import requests
import os
from fastapi import HTTPException, status

# This should be your Google Client ID
# Usually loaded from environment variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

def verify_google_token(token: str):
    """
    Verifies a Google ID token.
    Returns the user information if valid, raises HTTPException otherwise.
    """
    if not GOOGLE_CLIENT_ID:
        # For development, if no client ID is set, we might want to warn
        # or handle it differently.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google Client ID not configured in backend."
        )
        
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        # ID token is valid. Get the user's Google ID from the 'sub' claim.
        # idinfo contains: 'iss', 'sub', 'email', 'name', 'picture', etc.
        return idinfo
    except ValueError as e:
        # Invalid token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {str(e)}"
        )
