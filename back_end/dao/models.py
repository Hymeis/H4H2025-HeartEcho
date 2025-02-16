from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase
from flask_login import UserMixin

# Define the Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

class User(Base, UserMixin):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    post_list = Column(JSON, default=list)
    like_list = Column(JSON, default=list)

    # Relationships
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="commenter")


class Post(Base):
    __tablename__ = 'posts'

    pid = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.uid'), nullable=False)
    title = Column(String(120), nullable=False)
    content = Column(Text, nullable=False)
    tag = Column(String(50), nullable=False)
    user_nickname = Column(String(120), nullable=False)
    likes = Column(Integer, default=0)
    comment_list = Column(JSON, default=list)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = 'comments'

    cid = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.pid'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.uid'), nullable=False)
    content = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    comment_from = Column(Integer, default=-1)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    commenter = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Tag(Base):
    __tablename__ = 'tags'

    tid = Column(Integer, primary_key=True)
    category = Column(String(50), unique=True, nullable=False)