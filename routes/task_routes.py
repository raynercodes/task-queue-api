from flask import Blueprint, request, g
from services.task_services import create_task_for_user, get_tasks_for_user, get_task_by_id_for_user, get_task_stats_for_user
from utils.responses import success_response
from utils.auth import require_access_token

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks", methods=["POST"])
@require_access_token
def create_task_route():
    data = request.get_json() or {}

    result = create_task_for_user(
        g.user_id,
        data.get("task_type"),
        data.get("payload"),
    )

    return success_response(result, message="Task created successfully", status=201)

@tasks_bp.route("/tasks", methods=["GET"])
@require_access_token
def get_tasks_route():
    result = get_tasks_for_user(g.user_id)

    return success_response(result, message="Tasks retrieved successfully")

@tasks_bp.route("/tasks/<int:task_id>", methods=["GET"])
@require_access_token
def get_tasks_by_id_route(task_id):
    result = get_task_by_id_for_user(g.user_id, task_id)

    return success_response(result, message="Task retrieved successfully")

@tasks_bp.route("/tasks/stats", methods=["GET"])
@require_access_token
def get_task_stats_route():
    result = get_task_stats_for_user(g.user_id)

    return success_response(result, message="Tasks stats retrieved successfully")