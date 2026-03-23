
from fastapi.templating import Jinja2Templates
import pathlib

# templates = Jinja2Templates(directory="app/templates")

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
