import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "task-queue.db")
SECRET_KEY = "9a0e8d7w6f5q3l8g0b2m3c1v4n8q4l7z"
ACCESS_TOKEN_EXPIRE_MINUTES = 15