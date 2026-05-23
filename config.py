import os

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    PORT = int(os.getenv("PORT", 5000))