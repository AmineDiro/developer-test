import json

import pydantic
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings, SettingsConfigDict

from navigation.models import Empire
from navigation.solver import compute_arrival_odds
from navigation.utils import start_millennium_falcon


class Settings(BaseSettings):
    millennium_falcon_json: str
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
falcon, galaxy_map = start_millennium_falcon(settings.millennium_falcon_json)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health", include_in_schema=False)
def healthcheck():
    return {"message": "Healthy!"}


@app.post("/compute_odds")
async def compute_odds(request: Request, file: UploadFile = File(...)):
    content = await file.read()
    try:
        empire_data = json.loads(content)
        empire = Empire(**empire_data)

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Please submit a valid JSON file.")
    except pydantic.ValidationError:
        raise HTTPException(
            status_code=400,
            detail="We don't have time. Please give us the Empire's plan.",
        )

    odds = compute_arrival_odds(falcon, empire, galaxy_map)
    return templates.TemplateResponse(
        "odds.html",
        {"request": request, "odds": f"{odds*100:.2f}"},
    )
