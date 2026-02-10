from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import database
from schemas import models
from dependencies import get_db, get_current_admin_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

# Pydantic model for role update request
class RoleUpdate(BaseModel):
    role: str

@router.patch("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    role_update: RoleUpdate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    """
    Update a user's role. Only accessible by admin users.
    """
    # Validate role value
    valid_roles = ["user", "admin"]
    if role_update.role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}"
        )
    
    # Find the target user
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent admin from changing their own role (safety measure)
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role"
        )
    
    # Update the role
    old_role = user.role
    user.role = role_update.role
    db.commit()
    db.refresh(user)
    
    return {
        "message": f"User '{user.username}' role updated from '{old_role}' to '{role_update.role}'",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }

@router.get("/users", response_class=HTMLResponse)
def get_admin_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    
    rows = ""
    for user in users:
        rows += f"""
        <tr>
            <td>{user.id}</td>
            <td>{user.username}</td>
            <td>{user.email}</td>
            <td style="font-weight: bold; color: #6366f1;">{user.role}</td>
            <td style="font-family: monospace; font-size: 0.8em; color: #666;">{user.hashed_password[:20]}...</td>
        </tr>
        """
        
    html_content = f"""
    <html>
        <head>
            <title>Admin - Database Viewer</title>
            <style>
                body {{ font-family: sans-serif; padding: 40px; background: #f4f7f6; }}
                h1 {{ color: #333; }}
                table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #eee; }}
                th {{ background-color: #6366f1; color: white; }}
                tr:hover {{ background-color: #f9f9ff; }}
            </style>
        </head>
        <body>
            <h1>Registered Users</h1>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Password (Hash)</th>
                    </tr>
                </thead>
                <tbody>
                    {rows if rows else '<tr><td colspan="5" style="text-align:center;">No users found</td></tr>'}
                </tbody>
            </table>
            <br>
            <a href="/" style="color: #6366f1;">&larr; Back to App</a>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
