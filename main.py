import platform
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class ip(BaseModel):
    ip: str

@app.get("/")
async def root(r: Request):
    hostname = platform.node()
    data = r.headers.items() + \
        [("remoteAddr", r.client.host), ("remotePort", r.client.port)]
    return templates.TemplateResponse("index.html", {"request": r, 'hostname': hostname, "headers": data})

@app.get("api/v1/ip")
async def get_ip(r: Request):
    return {"IP": r.headers["x-real-ip"] if "x-real-ip" in r.headers.keys() else r.client.host}

@app.get("/api/v1/version")
async def version(r: Request):
    return {"Version": "version 3.0.0"}

@app.get("/metrics")
async def version(r: Request):
    data = r.headers.items() + \
        [("remoteAddr", r.client.host), ("remotePort", r.client.port)]
    return {"data": data}

@app.get("/health")
async def version(r: Request):
    return {"health": True}
