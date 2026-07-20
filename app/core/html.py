import bleach

_ALLOWED_TAGS = [
    "div",
    "br",
    "strong",
    "em",
    "a",
    "ul",
    "ol",
    "li",
]

_ALLOWED_ATTRIBUTES = {
    "a": [
        "href",
        "title",
    ],
}

_ALLOWED_PROTOCOLS = [
    "http",
    "https",
    "mailto",
]


def sanitize_html(html: str | None) -> str:
    if not html:
        return ""

    return bleach.clean(
        html,
        tags=_ALLOWED_TAGS,
        attributes=_ALLOWED_ATTRIBUTES,
        protocols=_ALLOWED_PROTOCOLS,
        strip=True,
    )