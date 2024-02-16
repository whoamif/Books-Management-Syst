from typing import Union

from fastapi import FastAPIt
from starlette.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates") 
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}