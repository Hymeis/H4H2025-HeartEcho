import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here' # Use environment variable or default

    # Database Configuration (MySQL)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+mysqlconnector://<username>:<password>@<host>:<port>/<database_name>'
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Disable modification tracking for performance