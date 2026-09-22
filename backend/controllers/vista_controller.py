import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["vistas"])

TEMPLATE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../frontend/templates")
)
templates = Jinja2Templates(directory=TEMPLATE_DIR)


@router.get("/", response_class=HTMLResponse)
@router.get("/login.html", response_class=HTMLResponse)
def mostrar_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/index.html", response_class=HTMLResponse)
def mostrar_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
