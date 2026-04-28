# Task Queue API

A backend API for managing asynchronous tasks with background processing, retry logic, and user-based ownership.

---

## Features

- JWT authentication (access + refresh tokens)
- Protected routes with user ownership (`g.user_id`)
- Create and manage tasks
- Background worker for async task processing
- Task lifecycle:
  - pending → processing → completed / failed
- Retry logic with max retry limits
- Task statistics endpoint (status counts)
- JSON payload support for flexible task data

---

## Tech Stack

- Python
- Flask
- SQLite
- PyJWT
- Werkzeug

---

## Project Structure
repos/
routes/
services/
utils/
app.py
worker.py
database.py
db.py
config.py

---

## How to Run

### Install dependencies
```bash
- pip install -r requirements.txt
- python database.py
- python app.py
- python worker.py

---

## Authentication

 - POST /register
 - POST /login
 - POST /refresh

 - Use the access token for all protected routes.

---

## Task Endpoints

 - POST /tasks
 - GET /tasks
 - GET /tasks/<id>
 - GET /tasks/stats

 ---

 ## Example Task

 {
  "task_type": "generate_report",
  "payload": {
    "report_name": "weekly",
    "fail": true
  }
}

---

## How to test:

- 1. Register a user:
    POST /register

- 2. Login:
    POST /login

- 3. Copy access token

- 4. Use token in headers:
    Authorization: Bearer <token>

- 5. Access protected routes like:
    GET /tasks

---

## Task Processing

- Tasks are created with status:
    pending


- The worker processes them:
    pending → processing → completed


- If failure occurs:
    processing → pending (retry)


- After max retries:
    processing → failed


---

## Design Decisions
- Layered Architecture
- Routes handle requests
- Services handle business logic
- Repositories handle SQL

### Background Worker

A separate worker continuously processes pending tasks, simulating real backend job queues.

### Retry Logic

Failed tasks are retried up to a configurable limit before being marked as permanently failed.

### Row-Level Ownership

All queries filter by user_id to enforce secure access to user data.

### Stats Aggregation

Uses grouped SQL queries (GROUP BY) to return task counts by status.

---

## Future Improvements
- Task cancellation endpoint
- Pagination for task listing

---

## Run with Docker

1. Build and start containers
```bash
docker compose up --build

---

## Note:
The background worker is implemented and runs locally/Docker. Deploying it on Render requires a paid worker instance.

---

Live API: https://task-queue-api-8slh.onrender.com

## Author

Leonardo Rayner