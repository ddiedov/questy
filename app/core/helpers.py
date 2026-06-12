def safe_next_url(next_url: str | None) -> str:
    if not next_url:
        return "/"
    if not next_url.startswith("/") or next_url.startswith("//"):
        return "/"
    return next_url

def normalize_form_booleans(data_dict, model):
    for field_name, field in model.model_fields.items():
        if field.annotation is bool:
            data_dict[field_name] = field_name in data_dict

    return data_dict