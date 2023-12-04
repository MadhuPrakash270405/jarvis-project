from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()


# Jinja2 Templates for serving HTML
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ... include your API routers
