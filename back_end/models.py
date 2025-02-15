from app import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    post_list = db.Column(db.JSON, default=[])  # List of post IDs created by the user
    like_list = db.Column(db.JSON, default=[])  # List of liked post IDs

    posts = db.relationship("Post", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="commenter", lazy=True)

class Post(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.uid"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tag = db.Column(db.String(50), nullable=False)  # Category for the post
    user_nickname = db.Column(db.String(120), nullable=False)  # Random or user-defined nickname
    likes = db.Column(db.Integer, default=0)  # Number of likes
    comment_list = db.Column(db.JSON, default=[])  # List of comment IDs
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship("Comment", backref="post", lazy=True)

class Comment(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.pid"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.uid"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)  # Number of likes
    comment_from = db.Column(db.Integer, default=-1)  # -1 for direct post comments, else CID of parent comment
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Tag(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), unique=True, nullable=False)  # Defined categories
