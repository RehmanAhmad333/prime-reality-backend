from contextlib import asynccontextmanager
from fastapi import FastAPI

from core.database import test_database_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    test_database_connection()
    yield


app = FastAPI(
    title="Prime Reality API",
    lifespan=lifespan
)