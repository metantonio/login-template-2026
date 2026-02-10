from sqlalchemy import Column, Integer, String

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255), nullable=True)  # Nullable for OAuth users
    role = Column(String(50), default="user")
    
    # OAuth specific fields
    auth_provider = Column(String(50), default="local")  # 'local' or 'google'
    oauth_id = Column(String(255), unique=True, index=True, nullable=True)
    avatar_url = Column(String(512), nullable=True)
