import platform
import psutil
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class ip(BaseModel):
    ip: str
    port: int

@app.get("/")
async def root(r: Request):
    hostname = platform.node()
    data = r.headers.items() + \
        [("remoteAddr", r.client.host), ("remotePort", r.client.port)]
    return templates.TemplateResponse("index.html", {"request": r, 'hostname': hostname, "headers": data})

@app.get("/api/v1/ip")
async def get_ip(r: Request):
    return {"IP": r.headers["x-real-ip"] if "x-real-ip" in r.headers.keys() else r.client.host}

@app.get("/api/v1/version")
async def version(r: Request):
    return {"Version": "version 1.0.0"}

@app.get("/metrics")
async def metrics(r: Request):
    return {
        "node_name": platform.node(),
        "processor": platform.processor(),
        "system": platform.system(),
        "cpu_percent": psutil.cpu_percent(),
        "cpu_count": psutil.cpu_count(),
        "memory": psutil.virtual_memory().percent,
        "x-real-ip" : r.headers["x-real-ip"] if "x-real-ip" in r.headers.keys() else r.client.host
    }

@app.get("/health")
async def health(r: Request):
    return {"health": True}
