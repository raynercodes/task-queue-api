from db import get_db
from utils.redis_client import redis_client

def create_user(username, password_hash, created_at):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (username, password_hash, created_at)
        VALUES (%s, %s, %s)
        """,
        (username, password_hash, created_at)
    )

    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, password_hash
        FROM users
        WHERE username = %s
        """,
        (username,)
    )

    row = cursor.fetchone()
    conn.close()

    return row

def store_refresh_token(user_id, token, created_at):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO refresh_tokens (user_id, token, created_at)
        VALUES (%s, %s, %s)
        """,
        (user_id, token, created_at)
    )

    conn.commit()
    conn.close()

def get_refresh_token_repo(token):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, user_id, token, created_at, revoked_at
        FROM refresh_tokens
        WHERE token = %s
        """,
        (token,)
    )

    row = cursor.fetchone()
    conn.close()

    return row

def blacklist_refresh_token(token):
    # Store in Redis for 7 days (604800 seconds) to match refresh token lifetime
    redis_client.setex(f"blacklist:{token}", 604800, "revoked")

def is_token_blacklisted(token):
    return redis_client.exists(f"blacklist:{token}") == 1

def revoke_refresh_token(revoked_at, token):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE refresh_tokens
        SET revoked_at = %s
        WHERE token = %s
        """,
        (revoked_at, token)
    )

    conn.commit()
    conn.close()