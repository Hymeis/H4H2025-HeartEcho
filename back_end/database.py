from app import db

def init_db():
    db.create_all()

if __name__ == "__main__":
    init_db()
