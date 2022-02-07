import uvicorn

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.binance_client import BinanceClient
from app.model_loader import ModelLoader


app = FastAPI(
    title="Serving Crypto Models",
    description="API to serve dynamically crypto models",
    version="1.0",
    openapi_url="/api/v1/openapi.json",
)

client = BinanceClient()
models = ModelLoader()


@app.get("/", include_in_schema=False)
async def home():
    """
    Home endpoint to redirect to docs.
    """
    return RedirectResponse("/docs")


@app.get("/predict", include_in_schema=True, tags=["serving"])
async def predict(currency: str, compare: str):
    """
    Predict endpoint.

    Parameters
    ----------
    currency: str
        Currency used in the model.
    compare: str
        Compare used in the model.
    
    Returns
    -------
    """
    model_name = f"{currency}_{compare}"
    symbol = "".join(model_name.split("_"))
    data = client.get_five_days_data(symbol)
    response = models.get_predictions(model_name, data)
    return {"prediction": float(response)}


@app.put("/update_models", include_in_schema=True, tags=["serving"])
async def update_model():
    """
    Update models endpoint.
    """
    models.update_model_files()
    return {"message": "All models have been updated."}


@app.put("/update_date", include_in_schema=True, tags=["serving"])
async def update_date():
    """
    Update date endpoint.
    """
    models.update_date()
    return {"message": "Date has been updated."}


@app.get("/check_models_number", include_in_schema=True, tags=["monitoring"])
async def check_models_number():
    """
    Check models number endpoint.
    """
    number_of_running_models = len(models.session_models)
    if number_of_running_models == 0:
        return {"message": "Warning: No models are running."}
    else:
        response = {
            "message": f"Number of running models: {number_of_running_models}",
            "models": [],
        }
        for model in models.session_models:
            response["models"].append(model)
        return response


@app.get("/healthz", status_code=200, include_in_schema=True, tags=["monitoring"])
async def healthz():
    """
    Healthz endpoint.
    """
    return {"status": "ok"}


@app.get("/readyz", status_code=200, include_in_schema=True, tags=["monitoring"])
async def readyz():
    """
    Readyz endpoint.
    """
    return {"status": "ready"}


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
