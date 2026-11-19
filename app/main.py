from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routes.weather import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Weather Intelligence API",
    description="Real-time weather information and search history.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/", tags=["System"])
def welcome() -> dict[str, str]:
    return {"message": "Welcome to the Weather Intelligence API"}


@app.get("/health", tags=["System"])
def health() -> dict[str, str]:
    return {"status": "ok"}

