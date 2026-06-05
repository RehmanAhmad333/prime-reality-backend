# Prime Reality Backend API

Luxury real estate platform backend with AI features.

## Tech Stack
- FastAPI (Python)
- PostgreSQL + PostGIS
- Redis + Celery (async tasks)
- AWS S3 (image storage)
- SendGrid (email)
- Docker

## Prerequisites
- Python 3.11+
- PostgreSQL with PostGIS
- Redis (for Celery)
- AWS account (S3 bucket)
- SendGrid account (API key)

## Installation

1. Clone repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your values
6. Run migrations: `alembic upgrade head`
7. Start server: `uvicorn app.main:app --reload`

## API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Running with Docker
```bash
docker-compose -f docker-compose.prod.yml up -d