"""
Settings for wagtail_drawio

All variables should be set in the project settings file.
"""

from django.conf import settings


def drawio_url_base():
    """
    Get the drawio URL from the settings
    """
    return getattr(settings, "WAGTAIL_DRAWIO_URL", "https://embed.diagrams.net")


def drawio_query_string():
    """
    Get the drawio query string from the settings
    """
    query_string = getattr(settings, "WAGTAIL_DRAWIO_QUERY_STRING", "ui=atlas&spin=1")

    if not query_string.startswith("?"):
        query_string = query_string[1:]

    if query_string.endswith("&"):
        query_string = query_string[:-1]

    return f"{query_string}&embed=1&modified=unsavedChanges&proto=json"


def drawio_url():
    """
    Get the drawio URL from the settings
    """
    return f"{drawio_url_base()}?{drawio_query_string()}"
