def apply_filters(query, filters, filter_map: dict):

    if not filters:
        return query

    for field, value in filters.model_dump(exclude_none=True).items():

        if field not in filter_map:
            continue

        handler = filter_map[field]

        # handler — функція або конфіг
        if callable(handler):
            query = handler(query, value)
        else:
            # простий eq
            query = query.eq(handler, value)

    return query