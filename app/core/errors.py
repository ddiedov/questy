from pydantic import ValidationError

def validation_errors_to_dict(exc):
    result = {}

    for error in exc.errors():
        field = error["loc"][0]

        result.setdefault(field, [])
        result[field].append(error["msg"])

    return result