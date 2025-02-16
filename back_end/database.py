from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker
from base import Base
# from models import User, Post, Comment, Tag


engine = None
Session = scoped_session(sessionmaker())

def init_db(app):
    print("db init called")
    global engine
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Session.configure(bind=engine)
    Base.metadata.create_all(bind=engine)
    # Use inspect to get table names
    inspector = inspect(engine)
    print("Tables after creation:", inspector.get_table_names())
    print("DB initialization completed")

