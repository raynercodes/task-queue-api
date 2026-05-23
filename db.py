import psycopg
from config import Config


def get_db():
    return psycopg.connect(Config.DATABASE_URL)