from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from .config import STATIC_DIR, get_settings
from .routes import router

logging.basicConfig(level=logging.INFO)

settings = get_settings()
app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
app.mount("/src", StaticFiles(directory=STATIC_DIR / "src"), name="src")
app.mount("/sample-data", StaticFiles(directory=STATIC_DIR / "sample-data"), name="sample-data")


@app.get("/", response_class=HTMLResponse)
def index():
    html = (STATIC_DIR / "index.html").read_text(encoding="utf-8")
    meta = f'<meta name="azure-maps-key" content="{settings.azure_maps_key or ""}" />'
    return html.replace("</head>", f"    {meta}\n  </head>")


@app.get("/{file_path:path}")
def static_file(file_path: str):
    target = STATIC_DIR / file_path
    if target.is_file():
        if target.suffix == ".html":
            return FileResponse(target, media_type="text/html")
        return FileResponse(target)
    raise HTTPException(status_code=404, detail="Not found")
