def checkFilters(filters):
    newFilters = {}
    for function, value in filters.items():
        if value:
            newFilters[function] = value
    return newFilters