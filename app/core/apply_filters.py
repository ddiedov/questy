from enum import Enum

def apply_filters(query, filters, filter_map: dict):
    if not filters:
        return query

    def normalize(value):
        if isinstance(value, Enum):
            return value.value
        return value

    data = filters.model_dump(exclude_none=True)

    for field, value in data.items():

        if field not in filter_map:
            continue

        value = normalize(value)

        handler = filter_map[field]

        # handler is a function or a column name.
        if callable(handler):
            query = handler(query, value)
        else:
            query = query.eq(handler, value)

    return query
