from fastapi import Request
from fastapi import APIRouter

from fastapi.templating import Jinja2Templates


router = APIRouter()

# Jinja2 Templates for serving HTML
templates = Jinja2Templates(directory="templates")



@router.get("/")
async def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})