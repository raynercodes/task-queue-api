from repos.task_repos import get_task_by_id, update_task_status, increment_retry_count
from utils.redis_client import redis_client
from datetime import datetime, UTC
import time
import json


def worker_loop():
    print("Worker is running...")

    while True:
        result = redis_client.blpop("task_queue", timeout=5)

        if not result:
            continue

        _, task_id = result
        task = None

        for _ in range(3):
            task = get_task_by_id(int(task_id))
            if task:
                break
            time.sleep(0.1)

        if not task:
            print(f"Task {task_id} not found in database after retries, skipping")
            continue

        task_id = task[0]
        task_type = task[2]
        payload = task[3]

        updated_at = datetime.now(UTC).isoformat()

        
        update_task_status(
            task_id,
            "processing",
            updated_at,
            error_message=None
            )

        try:
            payload_data = json.loads(payload) if payload else {}

            if not isinstance(payload_data, dict):
                raise ValueError("Payload must decode to a JSON object")
            
            fail_value = payload_data.get("fail")

            if fail_value is True or str(fail_value).lower() == "true":
                raise ValueError("Simulated task failure")
            
            if task_type == "send_email":
                time.sleep(3)
            elif task_type == "generate_report":
                time.sleep(5)
            elif task_type == "cleanup":
                time.sleep(2)
            else:
                raise ValueError(f"Unknown task type: {task_type}")
            
            updated_at = datetime.now(UTC).isoformat()

            update_task_status(
                task_id,
                "completed",
                updated_at,
                error_message=None,
            )

        except Exception as e:
            print(f"update_task_status crashed: {e}", flush=True)
            updated_at = datetime.now(UTC).isoformat()
            retry_count = task[8]
            max_retries = task[9]

            if retry_count < max_retries:
                increment_retry_count(task_id)

                update_task_status(
                    task_id,
                    "pending",
                    updated_at,
                    error_message=str(e)
                )
                redis_client.rpush("task_queue", task_id)
                print(f"Task {task_id} failed with error: {e}. Retrying ({retry_count + 1}/{max_retries})...")
            else:
                update_task_status(
                    task_id,
                    "failed",
                    updated_at,
                    error_message=str(e)
                )
                print(f"Task {task_id} permanently failed: {e}", flush=True)

if __name__ == "__main__":
    worker_loop()
