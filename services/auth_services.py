from repos.auth_repo import create_user, get_user_by_username, store_refresh_token, get_refresh_token_repo, revoke_refresh_token
from utils.auth import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, UTC

def register_user(username, password):
    username = (username or "").strip().lower()
    password = password or ""

    created_at = datetime.now(UTC).isoformat()

    if not username:
        raise ValueError("Username is required")
    
    if len(username) <= 3:
        raise ValueError("Username must be atleast 4 characters")
    
    if not password:
        raise ValueError("Password is required")
    
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters")
    
    existing = get_user_by_username(username)

    if existing:
        raise ValueError("User already exists")
    
    password_hash = generate_password_hash(password)

    create_user(username, password_hash, created_at)

    return {"username": username}

def login_user(username, password):
    username = (username or "").strip().lower()
    password = password or ""

    if not username:
        raise ValueError("Username is required")
    
    if not password:
        raise ValueError("Password is required")
    
    row = get_user_by_username(username)

    if row is None:
        raise ValueError("Invalid credentials")
    
    user_id, password_hash = row

    is_password = check_password_hash(password_hash, password)

    if not is_password:
        raise ValueError("Invalid credentials")
    
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token()
    created_at = datetime.now(UTC).isoformat()

    store_refresh_token(user_id, refresh_token, created_at)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

def refresh_access_token(refresh_token):
    refresh_token = (refresh_token or "").strip()

    if not refresh_token:
        raise ValueError("Refresh token is required")
    
    row = get_refresh_token_repo(refresh_token)

    if row is None:
        raise ValueError("Invalid refresh token")
    
    token_id, user_id, token, created_at, revoked_at = row

    if revoked_at is not None:
        raise ValueError("Invalid refresh token")
    
    revoked_time = datetime.now(UTC).isoformat()

    revoke_refresh_token(revoked_at, revoked_time)

    access_token = create_access_token(user_id)
    new_refresh_token = create_refresh_token()
    new_created_at = datetime.now(UTC).isoformat()

    store_refresh_token(user_id, new_refresh_token, new_created_at)

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token
    }