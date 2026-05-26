from bleach import clean


def sanitize_input(value: str):

    return clean(value)