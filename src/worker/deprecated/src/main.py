from celery.result import AsyncResult
from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import staticfiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from worker import create_task


app = FastAPI(
    title="Worker Launcher",
    description="Launch training workers easily",
    version="1.0",
    openapi_url="/api/v1/openapi.json",
)


@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse("/docs")


@app.get("/api/v1/launch_training", tags=["Training"])
def launch_trainer_to_training(currency: str, compare: str):
    pass
