from fastapi import Header, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from .api import app, db, get_user
from .schemas import *
from db.schemas import User, Like, DisLike

@app.post("/api/posts/{post_id}/like")
def like_post(user: User = Depends(get_user), post_id: int = 0, authorization: str = Header(...)):
    if authorization != user.token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    post = db.get_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    like = Like(user=user.username, post=post.id)
    db.add_like(like)
    return JSONResponse({"message": "Post liked"})

@app.post("/api/posts/{post_id}/dislike")
def dislike_post(user: User = Depends(get_user), post_id: int = 0, authorization: str = Header(...)):
    if authorization != user.token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    post = db.get_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    dislike = DisLike(user=user, post=post)
    db.add_dislike(dislike)
    return JSONResponse({"message": "Post disliked"})
