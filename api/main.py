import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from api.utils.db import MongoDbManager
from api.utils.logger import LoggingMiddleware
from api.utils.version import get_version
from api.routers import auth, ui, routes

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_manager = MongoDbManager()
    db = await db_manager.connect()
    app.state.db = db

    yield

    await db_manager.close()


app = FastAPI(
    root_path=os.getenv("ROOT_PATH", ""),
    lifespan=lifespan,
    title="Strava-routes API",
    version=get_version(),
    description="API for Strava-routes",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.include_router(ui.router)
app.include_router(auth.router)
app.include_router(routes.router)
