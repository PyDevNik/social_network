from fastapi import Body, Header, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from .api import app, db, get_user
from .schemas import *
from db.schemas import User, Post

@app.get("/api/posts")
def posts(user: User = Depends(get_user), authorization: str = Header(...)):
    if authorization != user.token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    posts =  [db.get_post(id).dict() for id in user.posts]
    return JSONResponse(posts)

@app.post("/api/posts")
def add_post(user: User = Depends(get_user), post: PostCreate = Body(), authorization: str = Header(...)):
    if authorization != user.token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    id=db.generate_id()
    post = Post(author=user.username, **post.dict(), id=id)
    user.posts.append(id)
    db.update_user(user)
    db.add_post(post)
    return JSONResponse(post.dict())

@app.put("/api/posts/{post_id}")
def edit_post(user: User = Depends(get_user), post_id: int = 0, updated_post: PostCreate = Body(), authorization: str = Header(...)):
    if authorization != user.token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    post = db.get_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.author != user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the author of this post")
    updated_post = Post(author=user.username, **updated_post.dict(), id=post.id)
    db.update_post(updated_post)
    db.update_user(user)
    return JSONResponse(updated_post.dict())

@app.delete("/api/posts/{post_id}")
def delete_post(user: User = Depends(get_user), post_id: int = 0, authorization: str = Header(...)):
    if authorization != user.token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    post = db.get_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.author != user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the author of this post")
    db.remove_post(post)
    return JSONResponse({"message": "Post deleted"})