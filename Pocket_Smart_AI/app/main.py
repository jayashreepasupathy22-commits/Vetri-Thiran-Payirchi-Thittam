from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from fastapi.staticfiles import (
    StaticFiles
)

from .config import settings

from .database import init_db

from .routers import (
    auth,
    planners,
    pages
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()

    yield


init_db()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=settings.CORS_ORIGINS,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


STATIC_DIR = (
    Path(__file__).resolve().parent
    .parent
    / "static"
)


app.mount(
    "/static",
    StaticFiles(
        directory=str(STATIC_DIR)
    ),
    name="static"
)


app.include_router(
    pages.router
)

app.include_router(
    auth.router
)

app.include_router(
    planners.router
)


@app.get("/api/health")
def health():

    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "gemini_configured":
            bool(settings.GEMINI_API_KEY),
        "model":
            settings.GEMINI_MODEL
    }


@app.post("/api/startup")
def startup():

    init_db()

    return {
        "status": "initialized"
    }