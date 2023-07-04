from fastapi import Body, HTTPException, status
from fastapi.responses import JSONResponse
from .api import app, db
from .schemas import *
from db.schemas import User

@app.post("/api/signup")
def signup(user: UserCreate = Body()):
    existing_user = db.get_user(email=user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    token = db.generate_token()
    user = User(token=token, **user.dict())
    db.add_user(user)
    return JSONResponse(user.dict())

@app.post("/api/login")
def login(credentials: UserLogin = Body()):
    user = db.get_user(email=credentials.email)
    if not user or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return JSONResponse(user.dict())