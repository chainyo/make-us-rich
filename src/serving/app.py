import uvicorn

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from model_loader import ModelLoader


app = FastAPI(
    title="Serving Crypto Models",
    description="API to serve dynamically crypto models",
    version="1.0",
    openapi_url="/api/v1/openapi.json",
)

model_loader = ModelLoader()


@app.get("/", include_in_schema=False)
async def home():
    """
    Home endpoint to redirect to docs.
    """
    return RedirectResponse("/docs")


@app.get("/predict", include_in_schema=True)
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
    response = model_loader.get_predictions(model_name)


@app.put("/update_models", include_in_schema=True)
async def update_model():
    """
    Update models endpoint.
    """
    model_loader.update_model_files()
    return {"message": "All models have been updated."}


@app.put("/update_date", include_in_schema=True)
async def update_date():
    """
    Update date endpoint.
    """
    model_loader.update_date()
    return {"message": "Date has been updated."}


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
