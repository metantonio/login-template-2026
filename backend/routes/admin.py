from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import database
from schemas import models

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
