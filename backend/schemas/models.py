from sqlalchemy import Column, Integer, String

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))  # Bcrypt hashes are ~60 chars, 255 provides ample room
    role = Column(String(50), default="user")
