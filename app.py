from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# ── Home / index route ──────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


# ── Prediction route (GET) ──────────────────────────────────────────────────
@app.get("/predictdata", response_class=HTMLResponse)
async def predict_datapoint_get(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"results": None}
    )


# ── Prediction route (POST) ─────────────────────────────────────────────────
@app.post("/predictdata", response_class=HTMLResponse)
async def predict_datapoint_post(
    request: Request,
    gender: str                      = Form(...),
    ethnicity: str                   = Form(...),
    parental_level_of_education: str = Form(...),
    lunch: str                       = Form(...),
    test_preparation_course: str     = Form(...),
    reading_score: float             = Form(...),
    writing_score: float             = Form(...),
):
    data = CustomData(
        gender=gender,
        race_ethnicity=ethnicity,
        parental_level_of_education=parental_level_of_education,
        lunch=lunch,
        test_preparation_course=test_preparation_course,
        reading_score=writing_score,   # swapped to match original Flask behaviour
        writing_score=reading_score,   # swapped to match original Flask behaviour
    )

    pred_df = data.get_data_as_data_frame()
    print(pred_df)

    predict_pipeline = PredictPipeline()
    results = predict_pipeline.predict(pred_df)

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"results": round(results[0], 2)}
    )


# ── Entry point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=80, reload=True)