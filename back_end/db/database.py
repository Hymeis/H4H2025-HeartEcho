from app import db

def init_db():
    from models import User, Post, Comment, Like, Tag
    db.create_all()

if __name__ == "__main__":
    init_db()
