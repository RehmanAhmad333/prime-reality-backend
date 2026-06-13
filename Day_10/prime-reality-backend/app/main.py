import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException 
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text
from app.core.database import engine
from app.api.v1.endpoints import auth, users, properties, saved, inquiries, bookings, platform, reviews, admin ,ai, alerts, chat

from app.core.rate_limit import limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Lifespan setup for startup and shutdown events.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Test database connection
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection successful")
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise  # Don't start app if DB is down
    
    yield  # App runs here
    
    engine.dispose()
    print("Database engine disposed")

# FastAPI instance  
app = FastAPI(
    title="Prime Reality API",
    version="1.0.0",
    lifespan=lifespan
)

app.state.limiter = limiter
app.add_exception_handler(HTTPException, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Load allowed origins from .env (comma-separated string)
# Default backup urls provided if env variable is missing
frontend_urls_str = os.getenv("FRONTEND_URLS", "http://localhost:5173,http://localhost:3000")
allowed_origins = [url.strip() for url in frontend_urls_str.split(",")]

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Router (Home testing route)
@app.get("/")
def read_root():
    return {"message": "Welcome to Prime Reality API v1.0.0"}

# Application Routers Include
app.include_router(auth.router, prefix="/api/v1")

app.include_router(users.router, prefix="/api/v1")

app.include_router(properties.router, prefix="/api/v1")
app.include_router(saved.router, prefix="/api/v1")
app.include_router(inquiries.router, prefix="/api/v1")
app.include_router(bookings.router, prefix="/api/v1")
app.include_router(platform.router, prefix="/api/v1")
app.include_router(reviews.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
# Include AI router
app.include_router(ai.router, prefix="/api/v1")
# Include alerts and chat routers
app.include_router(alerts.router, prefix="/api/v1")
# Chat router is included last to ensure it doesn't interfere with other routes, especially since it handles WebSocket connections which are more sensitive to routing order.
app.include_router(chat.router, prefix="/api/v1")