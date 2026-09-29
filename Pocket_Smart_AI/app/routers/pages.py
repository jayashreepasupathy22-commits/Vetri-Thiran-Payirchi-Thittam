from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()

TEMPLATES_DIR = (
	Path(__file__).resolve().parents[2]
	/ "templates"
)

templates = Jinja2Templates(
	directory=str(TEMPLATES_DIR)
)


def render_page(
	request: Request,
	template_name: str
):
	return templates.TemplateResponse(
		request=request,
		name=template_name
	)


@router.get("/")
def index(request: Request):
	return render_page(request, "index.html")


@router.get("/home-planner")
def home_planner(request: Request):
	return render_page(request, "home_planner.html")


@router.get("/party-planner")
def party_planner(request: Request):
	return render_page(request, "party_planner.html")


@router.get("/jewelry-planner")
def jewelry_planner(request: Request):
	return render_page(request, "jewelry_planner.html")


@router.get("/login")
def login(request: Request):
	return render_page(request, "login.html")


@router.get("/register")
def register(request: Request):
	return render_page(request, "register.html")


@router.get("/dashboard")
def dashboard(request: Request):
	return render_page(request, "dashboard.html")


@router.get("/history")
def history(request: Request):
	return render_page(request, "history.html")


@router.get("/testimonial")
def testimonial(request: Request):
	return render_page(request, "testimonial.html")
