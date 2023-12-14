from fastapi import Request
from fastapi import APIRouter

from fastapi.templating import Jinja2Templates


router = APIRouter()

# Jinja2 Templates for serving HTML
templates = Jinja2Templates(directory="templates")



@router.get("/register")
async def registration(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})