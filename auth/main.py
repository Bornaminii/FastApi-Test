from fastapi import FastAPI, Depends, HTTPException, status
from datetime import datetime, timedelta
from time import timezone
from jose import jwt
from sqlalchemy.orm import Session
from auth import model, schemas, utils
from auth_db import get_db
from fastapi.security import OAuth2PasswordRequestForm


SECRET_KEY = "6T4ncOHT03s21wYcQuwoKvTb6zm2tZTDuMt8TlVghnE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


app = FastAPI()


@app.post("/signup")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(model.User).filter(
        model.User.username == user.username).first()

    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = utils.hash_password(user.password)
    new_user = model.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "role": new_user.role
    }


@app.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(model.User).filter(
        model.User.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User does not exist")
