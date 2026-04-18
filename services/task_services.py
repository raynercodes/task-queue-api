from datetime import datetime, UTC
from repos.task_repos import create_task, list_tasks_by_user, get_task_by_id_for_user_repo
import json

ALLOWED_TASK_TYPES = {"send_email", "generate_report", "cleanup"}
ALLOWED_TASK_STATUSES = {"pending", "processing", "completed", "failed"}

def create_task_for_user(user_id, task_type, payload):
    task_type = (task_type or "").strip().lower()

    if task_type not in ALLOWED_TASK_TYPES:
        raise ValueError("Invalid task type")
    
    if payload is None or payload == "":
        raise ValueError("Payload cannot be empty")
    
    try:
        payload_json = json.dumps(payload)
    except (TypeError, ValueError):
        raise ValueError("Payload must be valid JSON data")
    
    status = "pending"
    error_message = None
    created_at = datetime.now(UTC).isoformat()
    updated_at = created_at

    create_task(
        user_id,
        task_type,
        payload_json,
        status,
        error_message,
        created_at,
        updated_at
    )

    return {
        "task_type": task_type,
        "payload": payload,
        "status": status,
        "created_at": created_at,
        "updated_at": updated_at
    }

def get_tasks_for_user(user_id):
    rows = list_tasks_by_user(user_id)

    tasks = [
        {
            "id": row[0],
            "user_id": row[1],
            "task_type": row[2],
            "payload": json.loads(row[3]) if row[3] else None,
            "status": row[4],
            "error_message": row[5],
            "created_at": row[6],
            "updated_at": row[7]
        }
        for row in rows
    ]

    return tasks

def get_task_by_id_for_user(user_id, task_id):
    try:
        task_id = int(task_id)
    except (TypeError, ValueError):
        raise ValueError("Task id must be a valid integer")

    row = get_task_by_id_for_user_repo(user_id, task_id)

    if row is None:
        raise ValueError("Task not found")
    
    task = {
            "id": row[0],
            "user_id": row[1],
            "task_type": row[2],
            "payload": json.loads(row[3]) if row[3] else None,
            "status": row[4],
            "error_message": row[5],
            "created_at": row[6],
            "updated_at": row[7]
        }

    return task