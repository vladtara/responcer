from fastapi import FastAPI, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(r: Request):
    return templates.TemplateResponse("index.html", {"request": r, "headers": r.headers.items()})


@app.get("/heders")
async def get_heder(r: Request):
    for i in r.headers.items():
        print(i[0], "=", i[1])
    return {'headers': list(r.headers.items())}
