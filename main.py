import platform
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(r: Request):
    hostname = platform.node()
    data = r.headers.items() + \
        [("remoteAddr", r.client.host), ("remotePort", r.client.port)]
    return templates.TemplateResponse("index.html", {"request": r, 'hostname': hostname, "headers": data})
