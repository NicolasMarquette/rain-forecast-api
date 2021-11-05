"""Errors responses."""

RESPONSES = {
    400: {"description": "Incorrect username or password"},
    401: {"description": "Not authenticated"},
    401: {"description": "The user doesn't have enough privileges"},
    403: {"description": "Could not validate credentials"},
}