# YouTube Clipper

App personal: pegás una URL de YouTube, indicás un rango de tiempo, y te devuelve un clip (.mp4) para descargar.

## Cómo funciona
- Backend en **FastAPI** (`app.py`) que usa **yt-dlp** para descargar solo el fragmento pedido y **ffmpeg** para cortarlo con precisión.
- Frontend simple en `frontend/index.html`.
- Todo corre en un contenedor Docker (`Dockerfile`), para que el host tenga ffmpeg disponible.

## 1. Probarlo en tu compu (opcional)

```bash
docker build -t youtube-clipper .
docker run -p 8000:8000 youtube-clipper
```

Abrí `http://localhost:8000` en el navegador.

## 2. Subirlo a GitHub

```bash
cd youtube-clipper
git init
git add .
git commit -m "youtube clipper"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/youtube-clipper.git
git push -u origin main
```

(Creá antes el repo vacío en GitHub, sin README, para que no choque con el push.)

## 3. Desplegarlo gratis en Render

1. Entrá a [render.com](https://render.com) y creá una cuenta (podés usar tu cuenta de GitHub para loguearte).
2. **New +** → **Web Service**.
3. Elegí el repo `youtube-clipper` que acabás de subir.
4. Render va a detectar el `Dockerfile` y el `render.yaml` automáticamente. Dejá todo por defecto (plan **Free**).
5. Click en **Create Web Service**. El primer build tarda unos minutos.
6. Cuando termine, te da una URL tipo `https://youtube-clipper-xxxx.onrender.com` — esa es tu app.

De ahí en más, cada vez que hagas `git push` a `main`, Render redespliega solo (`autoDeploy: true` en `render.yaml`).

> Nota: en el plan gratuito de Render, el servicio "duerme" si no se usa por un rato y tarda ~30s en despertar en el próximo request. Para uso personal no debería molestar.

## Límites que le puse
- Clips de hasta 10 minutos (evita que se cuelgue con algo gigante).
- Los archivos generados se borran al reiniciar el servidor, para no llenar el disco.

## Nota legal
Descargar/recortar videos de YouTube puede ir en contra de sus Términos de Servicio. Esta app es para uso personal y privado; no la uses para redistribuir contenido de terceros.
