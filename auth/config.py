import datetime
import os


class Config:
    DEBUG = True
    TESTING = True
    HOST = '0.0.0.0'
    PORT = 5000
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    SECRET_KEY = "SECRET_KEY"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
