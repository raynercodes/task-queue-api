# Task Queue API

A backend REST API for managing asynchronous tasks with background processing, retry logic, Redis message brokering, and user-based ownership.

---

## Live API

https://tasks.raynercodes.dev

---

## Features

- JWT authentication with access and refresh token rotation
- Redis message brokering via BLPOP for instant task pickup
- Redis token blacklisting with automatic TTL expiry
- Redis caching on aggregation endpoints
- Async background worker with retry logic
- Task lifecycle management — pending → processing → completed / failed
- PostgreSQL with optimized queries and row-level data isolation
- Structured logging for debugging and request tracing
- Dockerized with four services — API, worker, PostgreSQL, Redis

---

## Tech Stack

- Python
- Flask
- PostgreSQL
- Redis
- Docker / Docker Compose
- Nginx + Let's Encrypt SSL
- PyJWT
- Werkzeug

---

## Project Structure

```
routes/
services/
repos/
utils/
app.py
worker.py
database.py
config.py
Dockerfile
docker-compose.yml
```

---

## How to Run

### With Docker (recommended)

```bash
git clone https://github.com/raynercodes/task-queue-api.git
cd task-queue-api
cp .env.example .env  # add your secrets
docker compose up --build
```

### Manual Setup

```bash
pip install -r requirements.txt
python database.py
python app.py
python worker.py
```

---

## Environment Variables

```
DATABASE_URL=dbname=task_queue_api user=postgres password=postgres host=db port=5432
SECRET_KEY=your-secret-key
REDIS_URL=redis://redis:6379
PORT=5000
```

---

## Authentication

```
POST /register
POST /login
POST /refresh
```

Use the access token in all protected route headers:
```
Authorization: Bearer <access_token>
```

---

## Task Endpoints

```
POST  /tasks          Create a new task
GET   /tasks          List all tasks for the authenticated user
GET   /tasks/<id>     Get a specific task
GET   /tasks/stats    Get task counts by status
```

---

## Example Task

```json
{
  "task_type": "generate_report",
  "payload": {
    "report_name": "weekly"
  }
}
```

### Supported Task Types

| Task Type | Processing Time |
|-----------|----------------|
| `send_email` | 3 seconds |
| `generate_report` | 5 seconds |
| `cleanup` | 2 seconds |

---

## Task Processing Flow

```
Client creates task
        ↓
API inserts task into PostgreSQL
        ↓
Task ID pushed to Redis via RPUSH
        ↓
API returns immediately
        ↓
Worker wakes up via BLPOP
        ↓
Worker fetches full task from PostgreSQL
        ↓
Worker processes task and updates status
        ↓
On failure — retries up to max_retries
        ↓
Final status: completed or failed
```

---

## Redis Implementation

Redis serves three roles in this project:

- **Task queue** — task IDs are pushed to a Redis list on creation. The worker uses BLPOP to block and wait for new tasks instead of polling the database every 2 seconds
- **Token blacklist** — revoked refresh tokens are stored in Redis with automatic TTL expiry so they clean themselves up
- **Stats cache** — the stats aggregation endpoint caches results for 30 seconds to reduce repeated database hits

---

## Design Decisions

### Redis Over Database Polling
The original worker polled PostgreSQL every 2 seconds checking for pending tasks. This caused unnecessary database load even when there was nothing to do. BLPOP blocks and waits until a task arrives, eliminating polling entirely.

### Token Blacklisting with TTL
Revoked refresh tokens are stored in Redis with a 7 day TTL matching the token lifetime. Redis automatically deletes expired entries so there's no cleanup job needed.

### Layered Architecture
Routes handle requests. Services handle business logic. Repositories handle SQL. This separation keeps each layer independently maintainable.

### Row-Level Data Isolation
Every query filters by user_id so users can only access their own tasks regardless of the task ID passed in the request.

---

## Future Improvements

- Task cancellation endpoint
- Pagination for task listing
- WebSocket support for real-time task status updates

---

## Author

Leonardo Rayner
github.com/raynercodes
tasks.raynercodes.dev