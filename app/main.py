import os
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware

from DataModel import DataModel
from DataModel import DataModel_2
from PredictionModel import PredictionModel
from DataProcessing import DataProcessing

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
pred_model = PredictionModel("data/routes.json")
data_processing = DataProcessing()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "BASE_URL": os.getenv("BASE_URL", "http://localhost:8000/")
    })

@app.post("/comment/predict/model_emd")
def ask_prediction(data: DataModel):
    data_processed = data_processing.get_readability(data)

    return pred_model.predict(data_processed, 'emd')

@app.post("/comment/predict/model_rf")
def ask_prediction(data: DataModel):
    data_processed = data_processing.get_readability(data)
    print(data_processed)
    return pred_model.predict(data_processed, 'rf')

@app.post("/comment/predict/model_gb")
def ask_prediction(data: DataModel):
    data_processed = data_processing.get_readability(data)['readability']
    prediction_dict = pred_model.predict(data_processed, 'gb')
    # to json format
    prediction_dict['prediction'] = str(prediction_dict['prediction'])
    return prediction_dict
    

@app.post("/comment/scoring")
def ask_scoring(data: DataModel):
    return data_processing.get_scores(data)
    
@app.post("/comment/distributions")
def ask_distributions(data: DataModel):
    return data_processing.get_distributions(data)

@app.post("/comment/readability")
def ask_readability(data: DataModel):
    return data_processing.get_readability(data)
