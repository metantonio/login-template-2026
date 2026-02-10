from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database, auth_utils
from schemas import pydantic as schemas
from schemas import models
from dependencies import get_db, get_current_user

router = APIRouter(
    prefix="",
    tags=["auth"],
)

@router.get("/me", response_model=schemas.UserResponse)
def get_current_user_profile(current_user: models.User = Depends(get_current_user)):
    """
    Get the current authenticated user's profile.
    Requires valid JWT token in Authorization header.
    """
    return current_user

@router.post("/signup", response_model=schemas.UserWithToken)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = auth_utils.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create JWT token for auto-login
    access_token = auth_utils.create_access_token(data={"sub": new_user.username, "role": new_user.role})
    
    return {
        "user": new_user,
        "token": {"access_token": access_token, "token_type": "bearer"}
    }

from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth_utils.SECRET_KEY, algorithms=[auth_utils.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@router.get("/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    # Find user by username
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    
    if not user or not auth_utils.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create JWT token
    access_token = auth_utils.create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

from auth_google import verify_google_token

@router.post("/auth/google", response_model=schemas.UserWithToken)
def google_login(request: schemas.GoogleLoginRequest, db: Session = Depends(get_db)):
    """
    Handle Google Login/Signup.
    Verifies the Google token, finds or creates the user, and issues a local JWT.
    """
    # 1. Verify Google token
    idinfo = verify_google_token(request.token)
    
    email = idinfo.get("email")
    google_id = idinfo.get("sub")
    name = idinfo.get("name")
    picture = idinfo.get("picture")
    
    # 2. Check if user exists (by email or oauth_id)
    user = db.query(models.User).filter(
        (models.User.email == email) | (models.User.oauth_id == google_id)
    ).first()
    
    if not user:
        # Create new user
        # We use email as username for Google users if not taken, otherwise add a suffix
        username_base = email.split("@")[0]
        username = username_base
        counter = 1
        while db.query(models.User).filter(models.User.username == username).first():
            username = f"{username_base}{counter}"
            counter += 1
            
        user = models.User(
            username=username,
            email=email,
            auth_provider="google",
            oauth_id=google_id,
            avatar_url=picture,
            role="user" # Default role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Update existing user info from Google if necessary
        user.oauth_id = google_id
        user.auth_provider = "google"
        user.avatar_url = picture
        db.commit()
        db.refresh(user)
        
    # 3. Create access token
    access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": user.username, "role": user.role}, 
        expires_delta=access_token_expires
    )
    
    return {
        "user": user,
        "token": {"access_token": access_token, "token_type": "bearer"}
    }
