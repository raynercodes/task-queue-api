from db import get_db

def create_task(user_id, task_type, payload, status, error_message, created_at, updated_at):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (user_id, task_type, payload, status, error_message, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (user_id, task_type, payload, status, error_message, created_at, updated_at)
    )

    conn.commit()
    conn.close()

def list_tasks_by_user(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
        id,
        user_id,
        task_type,
        payload,
        status,
        error_message,
        created_at,
        updated_at
        FROM tasks
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_task_by_id_for_user_repo(user_id, task_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, user_id, task_type, payload, status, error_message, created_at, updated_at
        FROM tasks
        WHERE user_id = %s AND id = %s
        """,
        (user_id, task_id)
    )

    row = cursor.fetchone()
    conn.close()

    return row

def get_next_pending_task():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, user_id, task_type, payload, status, error_message, created_at, updated_at, retry_count, max_retries
        FROM tasks
        WHERE status = 'pending'
        ORDER BY created_at ASC
        LIMIT 1
        """
    )

    row = cursor.fetchone()
    conn.close()
    return row

def update_task_status(task_id, status, updated_at, error_message=None):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET status = %s, updated_at = %s, error_message = %s
        WHERE id = %s
        """,
        (status, updated_at, error_message, task_id)
    )

    conn.commit()
    conn.close()

def get_task_stats_for_user_repo(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status, COUNT(*)
        FROM tasks
        WHERE user_id = %s
        GROUP BY status
        """,
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows

def increment_retry_count(task_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET retry_count = retry_count + 1
        WHERE id = %s
        """,
        (task_id,)
    )

    conn.commit()
    conn.close