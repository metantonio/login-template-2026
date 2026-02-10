#!/usr/bin/env python3
"""
Script to promote user with ID 1 to admin role.
Usage: python make_admin.py
"""

from database import SessionLocal
from schemas.models import User

def make_user_admin(user_id: int = 1):
    """
    Promote a user to admin role.
    
    Args:
        user_id: The ID of the user to promote (default: 1)
    """
    db = SessionLocal()
    try:
        # Find the user
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            print(f"❌ Error: User with ID {user_id} not found.")
            print("💡 Tip: Make sure you have registered at least one user first.")
            return False
        
        # Check if already admin
        if user.role == "admin":
            print(f"ℹ️  User '{user.username}' (ID: {user_id}) is already an admin.")
            return True
        
        # Update to admin
        old_role = user.role
        user.role = "admin"
        db.commit()
        
        print(f"✅ Success! User '{user.username}' (ID: {user_id}) promoted from '{old_role}' to 'admin'.")
        print(f"📧 Email: {user.email}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Admin Role Assignment Script")
    print("=" * 50)
    make_user_admin(user_id=1)
