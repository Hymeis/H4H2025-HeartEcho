from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker, scoped_session


url_object = URL.create(
        "mysql+mysqlconnector",
        username="root",
        password="12345",
        host="localhost",
        port="3306",
        database="heartecho",
    )

# Create the SQLAlchemy engine
engine = create_engine(url_object,
                       echo="debug",
                       pool_size=25,
                       pool_pre_ping=True,
                       pool_recycle=3600)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
db_session = scoped_session(Session)

def init_db():
    import back_end.dao.models as model
    model.Base.metadata.create_all(bind=engine)
