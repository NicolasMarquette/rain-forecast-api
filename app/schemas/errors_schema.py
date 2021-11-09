"""Errors responses."""

RESPONSES = {
    400: {"description": "Incorrect username or password"},
    401: {"description": "Not authenticated"},
    403: {"description": "Incorrect rights"},
    500: {"description": "Incorrect data format"}
}