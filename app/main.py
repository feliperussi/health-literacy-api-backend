import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

from app.DataModel import DataModel, DataModel_2
from app.PredictionModel import PredictionModel
from app.DataProcessing import DataProcessing

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

pred_model = PredictionModel("app/data/routes.json")
data_processing = DataProcessing()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "BASE_URL": os.getenv("BASE_URL", "http://localhost:8000/")
    })

def convert_numpy_types(data):
    """
    Convert numpy data types to native Python types for JSON serialization.
    """
    if isinstance(data, dict):
        return {k: convert_numpy_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_types(item) for item in data]
    elif isinstance(data, np.integer):
        return int(data)
    elif isinstance(data, np.floating):
        return float(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()
    else:
        return data

@app.post("/comment/predict/model_emd")
async def ask_prediction_emd(data: DataModel):
    data_processed = data_processing.get_readability(data)
    prediction = pred_model.predict(data_processed, 'emd')
    return convert_numpy_types(prediction)

@app.post("/comment/predict/model_rf")
async def ask_prediction_rf(data: DataModel):
    data_processed = data_processing.get_readability(data)
    prediction = pred_model.predict(data_processed, 'rf')
    return convert_numpy_types(prediction)

@app.post("/comment/predict/model_gb")
async def ask_prediction_gb(data: DataModel):
    data_processed = data_processing.get_readability(data)['readability']
    prediction_dict = pred_model.predict(data_processed, 'gb')
    prediction_dict['prediction'] = str(prediction_dict['prediction'])
    return convert_numpy_types(prediction_dict)

@app.post("/comment/scoring")
async def ask_scoring(data: DataModel):
    return convert_numpy_types(data_processing.get_scores(data))

@app.post("/comment/distributions")
async def ask_distributions(data: DataModel):
    return convert_numpy_types(data_processing.get_distributions(data))

@app.post("/comment/readability")
async def ask_readability(data: DataModel):
    return convert_numpy_types(data_processing.get_readability(data))
