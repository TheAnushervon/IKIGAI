from fastapi import FastAPI
from fastapi import Request
from fastapi import Form
from fastapi import UploadFile
from fastapi import File
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import aiohttp
import shutil
import os

app = FastAPI()
templates = Jinja2Templates(directory="pseudo_frontend/templates/")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit")
async def submit_form(request: Request,
                      inn: int = Form(...),
                      ukep: UploadFile = File(...),
                      mchd: Optional[UploadFile] = File(None),
                      email: str = Form(...),
                      confirmed: bool = Form(...)):
    # Save the uploaded file to a temporary directory
    ukep_path = f"temp/{ukep.filename}"
    os.makedirs(os.path.dirname(ukep_path), exist_ok=True)
    with open(ukep_path, "wb") as buffer:
        shutil.copyfileobj(ukep.file, buffer)

    if mchd:
        mchd_path = f"temp/{mchd.filename}"
        os.makedirs(os.path.dirname(mchd_path), exist_ok=True)
        with open(mchd_path, "wb") as buffer:
            shutil.copyfileobj(mchd.file, buffer)

    bos_payload = {
        "INN": inn,
        "UKEP": "",
        "MCHD": "",
        "e-mail": email
    }

    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8000/api/input/', json={"_BOS_": bos_payload}) as response1:
            response1_data = await response1.json()

    os.remove(ukep_path)

    return {
        "endpoint1_response": response1_data
    }
