from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = FastAPI()

templates = Jinja2Templates(directory="templates")


# ── Home / index route ──────────────────────────────────────────────────────
@application.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


# ── Prediction route (GET) ──────────────────────────────────────────────────
@application.get("/predictdata", response_class=HTMLResponse)
async def predict_datapoint_get(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"results": None}
    )


# ── Prediction route (POST) ─────────────────────────────────────────────────
@application.post("/predictdata", response_class=HTMLResponse)
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
        reading_score=reading_score,
        writing_score=writing_score,
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