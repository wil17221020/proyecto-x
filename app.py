import os
import uuid
import shutil

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import yt_dlp

app = FastAPI(title="YouTube Clipper")

CLIPS_DIR = "clips"
os.makedirs(CLIPS_DIR, exist_ok=True)

# Sirve el frontend estático en /static y la home redirige a index.html
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def root():
    return FileResponse("frontend/index.html")


def _time_to_sec(t: str) -> int:
    """Convierte 'HH:MM:SS', 'MM:SS' o 'SS' a segundos."""
    parts = [p.strip() for p in t.split(":")]
    if not all(p.isdigit() for p in parts):
        raise HTTPException(status_code=400, detail=f"Formato de tiempo inválido: {t}")
    parts = [int(p) for p in parts]
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, s = parts
    return h * 3600 + m * 60 + s


@app.get("/clip")
def get_clip(
    url: str = Query(..., description="URL del video de YouTube"),
    start: str = Query(..., description="Tiempo de inicio, ej: 00:01:30"),
    end: str = Query(..., description="Tiempo de fin, ej: 00:01:45"),
):
    start_sec = _time_to_sec(start)
    end_sec = _time_to_sec(end)
    if end_sec <= start_sec:
        raise HTTPException(status_code=400, detail="El tiempo final debe ser mayor al inicial")
    if end_sec - start_sec > 60 * 10:
        raise HTTPException(status_code=400, detail="El clip no puede durar más de 10 minutos")

    clip_id = str(uuid.uuid4())
    out_template = os.path.join(CLIPS_DIR, f"{clip_id}.%(ext)s")

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": out_template,
        "download_ranges": yt_dlp.utils.download_range_func(None, [(start_sec, end_sec)]),
        "force_keyframes_at_cuts": True,
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No se pudo procesar el video: {e}")

    files = [f for f in os.listdir(CLIPS_DIR) if f.startswith(clip_id)]
    if not files:
        raise HTTPException(status_code=500, detail="No se generó ningún archivo de clip")

    filepath = os.path.join(CLIPS_DIR, files[0])
    filename = f"clip_{start.replace(':', '-')}_{end.replace(':', '-')}.mp4"
    return FileResponse(filepath, filename=filename, media_type="video/mp4")


@app.on_event("startup")
def clean_old_clips():
    # Limpia clips viejos al arrancar para no llenar el disco del host
    shutil.rmtree(CLIPS_DIR, ignore_errors=True)
    os.makedirs(CLIPS_DIR, exist_ok=True)
