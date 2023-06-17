from fastapi import routing, Depends, HTTPException, status, Request, Form
from app.db.settings import SessionLocal
from app.db.models import User
from app.models.users import LoginUser

router = routing.APIRouter(prefix="/users", tags=["users"])


@router.post("/new")
def create_user(username: str, password: str, email: str):
    """Create a new user"""
    db = SessionLocal()

    user = User(username=username, password=password, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully"}


@router.get("/all")
def get_all_users():
    """Fetch all users"""
    db = SessionLocal()

    users = db.query(User).all()
    return users


@router.post("/login")
def login(userdetails: LoginUser):
    """Login a user"""
    db = SessionLocal()
    username = userdetails.username
    password = userdetails.password
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password != password:
        print("wrong password")
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"message": "User logged in successfully"}
