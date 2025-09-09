# Cloud-Native Todo/Job API

A production-style **FastAPI** project showcasing **backend, cloud, and DevOps skills**. It demonstrates RESTful API design, database persistence, authentication, caching, and containerized deployment.

-----

## 🚀 Features

  - CRUD operations for Todos (create, read, update, delete)
  - User authentication with JWT (registration & login)
  - Role-based access (admin vs user)
  - PostgreSQL database with Alembic migrations
  - Redis caching for GET endpoints (CACHE HIT/MISS logs included)
  - Docker & Docker Compose setup (FastAPI + Postgres + Redis)
  - Cloud-ready architecture (designed for AWS ECS + RDS + ElastiCache)

-----

## 🛠️ Tech Stack

  - **Backend**: FastAPI, SQLAlchemy, Alembic
  - **Database**: PostgreSQL (fallback to SQLite in local dev)
  - **Caching**: Redis
  - **Auth**: JWT (OAuth2 password flow)
  - **DevOps**: Docker, Docker Compose
  - **Cloud Design**: AWS ECS (Fargate), RDS, ElastiCache

-----

## ⚙️ Setup Instructions

### Local Development (SQLite)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

App runs at: `http://127.0.0.1:8000/docs`

### With Docker (Postgres + Redis)

```bash
docker compose up --build
```

FastAPI → `http://localhost:8000/docs`
Postgres → `localhost:5432`
Redis → `localhost:6379`

-----

## 🔑 Environment Variables

Create a `.env` file for secrets:

```env
DATABASE_URL=postgresql://user:password@db:5432/todo_db
REDIS_URL=redis://redis:6379/0
JWT_SECRET=your_secret_key
```

-----

## 📦 Migrations

Generate new migration:

```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:

```bash
alembic upgrade head
```

-----

## 🧪 Quick Test (Redis Cache Demo)

```bash
# Clear Redis cache
docker compose exec redis redis-cli FLUSHALL

# First request -> CACHE MISS (fetches from DB)
curl http://127.0.0.1:8000/todos/1

# Second request -> CACHE HIT (returns from Redis)
curl http://127.0.0.1:8000/todos/1
```

-----

## ☁️ Deployment (AWS Design)

  - FastAPI container → **ECS Fargate**
  - Postgres → **RDS**
  - Redis → **ElastiCache**
  - Secrets managed via **AWS SSM** or **Secrets Manager**
  - Logs/metrics via **CloudWatch**

-----

## ✨ Learning Goals

This project was built to demonstrate:

  - Building and securing REST APIs
  - Integrating databases with migrations
  - Using Redis for caching
  - Containerization and orchestration
  - Designing a production-ready AWS architecture

-----

## 📜 License

[MIT License](https://www.google.com/search?q=LICENSE)
