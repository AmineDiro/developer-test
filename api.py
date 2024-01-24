import json
from typing import Tuple

import pydantic
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.responses import FileResponse

from navigation.models import Empire
from navigation.solver import compute_arrival_odds
from navigation.utils import start_millennium_falcon


class Settings(BaseSettings):
    millennium_falcon_json: str
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
falcon, galaxy_map = start_millennium_falcon(settings.millennium_falcon_json)
app = FastAPI()

# app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.get("/")
async def main():
    return FileResponse("static/index.html")


@app.post("/compute_odds")
async def compute_odds(file: UploadFile = File(...)):
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
    return {"odds": odds}
