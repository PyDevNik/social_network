import os, sys
sys.path.append(os.path.join(sys.path[0], '..'))

from fastapi import FastAPI, Header, HTTPException, status
from db.db import DB

app = FastAPI()
db = DB()

def get_user(authorization: str = Header(...)):
    user = db.get_user(token=authorization)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user

from .users import *
from .posts import *
from .likes_and_dislikes import *