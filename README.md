# notification-service

Notification microservice for **Eldorado**, a marketplace platform built using FastAPI.

This service handles email-based notifications such as account verification, password resets, and other system messages. It’s designed to be decoupled from business logic and consumed by other services via REST or message queue.

---

## 🔧 Stack

- **FastAPI** — async Python web framework
- **AioSMTP / aiosmtplib** — async email delivery
- **Redis (optional)** — for queueing/scheduling (e.g., with Celery)
- **Docker** — containerized development
- **dotenv** — environment variable management

---

## 🚀 Features

- Send verification and notification emails
- Email templates with Jinja2 (or plain text fallback)
- Async email sending with retries
- Modular notification handling (e.g., `email_verification`, `task_alert`)
- Can be triggered by other services (HTTP or pub/sub)

---

## 🛠️ Local Development

### 1. Set up `.env`

```bash
./scripts/setup-env.sh
```

### 2. Start backend
```bash
./scripts/start-dev.sh
```
