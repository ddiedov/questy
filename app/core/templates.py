
from fastapi.templating import Jinja2Templates
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

import hashlib

def gravatar_hash(email):
    return hashlib.md5(email.lower().encode()).hexdigest()

templates.env.filters["gravatar"] = gravatar_hash