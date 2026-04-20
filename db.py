import psycopg
from config import DATABASE_URL


def get_db():
    return psycopg.connect(DATABASE_URL)