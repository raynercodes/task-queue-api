from repos.task_repos import get_next_pending_task, update_task_status, increment_retry_count
from datetime import datetime, UTC
import time
import json


def worker_loop():
    print("Worker is running...")

    while True:
        task = get_next_pending_task()

        if not task:
            time.sleep(2)
            continue

        task_id = task[0]
        task_type = task[2]
        payload = task[3]

        updated_at = datetime.now(UTC).isoformat()

        update_task_status (
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

            if fail_value is True or str(fail_value).strip().lower() == "true":
                raise Exception("Simulated failure")

            if task_type == "send_email":
                time.sleep(3)

            elif task_type == "generate_report":
                time.sleep(5)

            elif task_type == "cleanup":
                time.sleep(2)

            else:
                raise ValueError("Unknown task type")
            
            updated_at = datetime.now(UTC).isoformat()

            update_task_status(
                task_id,
                "completed",
                updated_at,
                error_message=None
            )
        except Exception as e:
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

                print(f"Current retry count {retry_count}")
            else:
                update_task_status(
                    task_id,
                    "failed",
                    updated_at,
                    error_message=str(e)
                )

        time.sleep(2)
    
if __name__ == "__main__":
    worker_loop()
