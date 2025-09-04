

import uvicorn
import platform
import psutil
import pathlib
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


app: FastAPI = FastAPI()
app.mount(
    path="/static",
    app=StaticFiles(directory=pathlib.Path(__file__).parent / "static"),
    name="static",
)


templates: Jinja2Templates = Jinja2Templates(directory=pathlib.Path(__file__).parent / "templates")


class ip(BaseModel):
    ip: str
    port: int


def help_get_ip(r: Request):
    return {
        "IP": (
            r.headers["x-real-ip"] if "x-real-ip" in r.headers.keys() else r.client.host # pyright: ignore[reportOptionalMemberAccess]
        )
    }

@app.get(path="/")
async def root(r: Request) :
    hostname: str = platform.node()
    real_ip: dict[str, str] = help_get_ip(r)
    data= r.headers.items() + [
        ("remoteAddr", r.client.host), # pyright: ignore[reportOptionalMemberAccess]
        ("remotePort", r.client.port), # pyright: ignore[reportOptionalMemberAccess]
    ]
    return templates.TemplateResponse(
        "index.html", {"request": r, "ip": real_ip["IP"] ,"hostname": hostname, "headers": data}
    )


@app.get(path="/api/v1/ip")
async def get_ip(r: Request) -> dict[str, str]:
    return help_get_ip(r)

@app.get(path="/api/v1/version")
async def version(r: Request) -> dict[str, str]:
    print(r)
    return {"Version": "version 1.0.0"}


@app.get(path="/metrics")
async def metrics(r: Request) -> dict[str, str | float | int | None]:
    return {
        "node_name": platform.node(),
        "processor": platform.processor(),
        "system": platform.system(),
        "cpu_percent": psutil.cpu_percent(),
        "cpu_count": psutil.cpu_count(),
        "memory": psutil.virtual_memory().percent,  # pyright: ignore[reportAny]
        "x-real-ip": help_get_ip(r)["IP"]
    }


@app.get(path="/health")
async def health(r: Request) -> dict[str, bool]:
    print(r)
    return {"health": True}


def main() -> None:

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
