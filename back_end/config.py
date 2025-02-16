import os

class Config:
    #SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here' # Use environment variable or default

    # Database Configuration (MySQL)
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:hanqingwang@localhost:3306/heartecho'
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Disable modification tracking for performance