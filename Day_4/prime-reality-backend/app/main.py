from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text
from app.core.database import engine
from app.api.v1.endpoints import auth  , users , properties

# Lifespan setup for startup and shutdown events. Isme hum database connection test karenge startup pe, aur shutdown pe database engine ko dispose karenge. Lifespan function ek async generator hai jo app ke lifecycle events ko manage karta hai. Startup me hum database connection test karte hain, aur agar connection successful hota hai to app start hota hai. Agar connection fail hota hai to exception raise hota hai aur app start nahi hota. Shutdown me hum database engine ko dispose karte hain taki resources release ho jayein.
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

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Router (Home testing route)
@app.get("/")
def read_root():
    return {"message": "Welcome to Prime Reality API v1.0.0"}

# 5. Application Routers Include
app.include_router(auth.router, prefix="/api/v1")
# 6. Future Routers (e.g., users, properties, chat) can be included here similarly
app.include_router(users.router, prefix="/api/v1") 

app.include_router(properties.router, prefix="/api/v1") 