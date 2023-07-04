from pymongo import MongoClient
from typing import List

import random
import string

from db.config import *
from .schemas import User, Post, Like, DisLike

class DB:
    def __init__(self) -> None:
        self.__client = MongoClient(url)
        self._db = self.__client.get_database(db_name)
        self._users = self._db.get_collection(users_collection)
        self._posts = self._db.get_collection(posts_collection)
        self._token_length = token_length
        self._id_length = id_length

    def generate_token(self) -> str:
        def generate():
            return "".join([random.choice(string.ascii_letters) for _ in range(self._token_length)])
        users = [user["token"] for user in self.get_all_users()]
        token = generate()
        while token in users:
            token = generate()
        return token
    
    def generate_id(self) -> str:
        def generate():
            return random.randint(int(f"1{'0'*(self._id_length-1)}"), int('9'*self._id_length))
        id = generate()
        posts = self.get_all_posts()
        likes = [post.likes for post in posts]
        dislikes = [post.dislikes for post in posts]
        while id in posts \
        or id in likes \
        or id in dislikes:
            id = generate()
        return id
    

    def add_user(self, user: User) -> None:
        self._users.insert_one(user.dict())

    def get_user(self, **kwargs) -> User:
        user_dict = self._users.find_one(kwargs)
        return User(**user_dict) if user_dict else None
    
    def update_user(self, user: User) -> None:
        filter = {"token": user.token}
        self._users.update_one(filter, {"$set": user.dict()})
    
    def get_all_users(self) -> List[User]:
        return [User(**data) for data in list(self._users.find())]


    def get_post(self, post_id: int) -> Post:
        post_dict = self._posts.find_one({"id": post_id})
        return Post(**post_dict) if post_dict else None

    def add_post(self, post: Post) -> None:
        self._posts.insert_one(post.dict())

    def update_post(self, post: Post) -> None:
        filter = {"id": post.id}
        self._posts.update_one(filter, {"$set": post.dict()})

    def remove_post(self, user: User, post: Post) -> None:
        self._posts.delete_one({"id": post.id})
        user.posts.remove(post.id)
        self.update_user(user)

    def get_all_posts(self) -> List[Post]:
        return [Post(**data) for data in list(self._posts.find())]


    def add_like(self, like: Like) -> None:
        post = self.get_post(like.post)
        if like.user in post.dislikes:
            post.dislikes.remove(like.user)
        post.likes.append(like.user)
        self.update_post(post)

    def add_dislike(self, dislike: DisLike) -> None:
        post = self.get_post(dislike.post)
        if dislike.user in post.likes:
            post.likes.remove(dislike.user)
        post.dislikes.append(dislike.user)
        self.update_post(post)

    def cancel_like(self, like: Like) -> None:
        post = self.get_post(like.post)
        if like.user in post.likes:
            post.dislikes.remove(like.user)
        self.update_post(post)

    def cancel_dislike(self, dislike: DisLike) -> None:
        post = self.get_post(dislike.post)
        if dislike.user in post.dislikes:
            post.dislikes.remove(dislike.user)
        self.update_post(post)
