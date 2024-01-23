import json

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# app.mount("/", StaticFiles(directory="static", html=True), name="static")

from starlette.responses import FileResponse


@app.get("/")
async def read_index():
    return FileResponse("static/index.html")


# Route to handle file upload and validation
@app.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        # Read the contents of the uploaded JSON file
        content = await file.read()
        json_data = json.loads(content)

        print(json_data)
        # Validate JSON (add your custom validation logic here)
        # # For example, checking if the JSON has a key named "data"
        # if "data" not in json_data:
        #     raise HTTPException(status_code=400, detail="Invalid JSON format")

        # If validation is successful, return "OK"
        return {"status": "OK"}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
