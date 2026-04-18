from flask import Blueprint, request
from services.auth_services import register_user, login_user, refresh_access_token
from utils.responses import success_response

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register_user_route():
    data = request.get_json() or {}

    result = register_user(data.get("username"), data.get("password"))

    return success_response(result, message="User created successfully", status=201)

@auth_bp.route("/login", methods=["POST"])
def login_user_route():
    data = request.get_json() or {}

    result = login_user(data.get("username"), data.get("password"))

    return success_response(result, message="Logged in successfully")

@auth_bp.route("/refresh", methods=["POST"])
def refresh_user():
    data = request.get_json() or {}

    result = refresh_access_token(data.get("refresh_token"))

    return success_response(result, message="Tokens refreshed successfully")