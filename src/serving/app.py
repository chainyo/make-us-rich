import onnx 
import onnxruntime 
import uvicorn

from fastapi import FastAPI
from starlette.responses import RedirectResponse


app = FastAPI(
    title="Serving Crypto Models",
    description="API to serve dynamically crypto models",
    version="1.0",
    openapi_url="/api/v1/openapi.json",
)


@app.get("/", include_in_schema=False)
async def home():
    """
    Home endpoint to redirect to docs.
    """
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run("serving.app:app", reload=True)
