from fastapi.templating import Jinja2Templates
import pathlib
import hashlib

from app.core.constants import PROPERTY_OPTIONS, PROPERTY_DEFAULTS

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=BASE_DIR / "templates")


def gravatar_hash(email):
    return hashlib.md5(email.lower().encode()).hexdigest()


def get_choice(choices, value):
    for choice in choices:
        if choice.id == value:
            return choice
    return None


templates.env.filters["gravatar"] = gravatar_hash

templates.env.globals.update(
    PROPERTY_OPTIONS=PROPERTY_OPTIONS,
    PROPERTY_DEFAULTS=PROPERTY_DEFAULTS,
    get_choice=get_choice,
)