"""
API Hooks for Wagtail
Adding edit pages for images

This code is distributed under the MIT License
"""

from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSetGroup

from .snippets import DrawioImageSnippetViewSet


class DrawioImageSnippetViewSetGroup(SnippetViewSetGroup):
    """Adding a group for Drawio image models"""

    menu_label = "Drawio"
    menu_icon = "drawio"

    items = (DrawioImageSnippetViewSet,)


register_snippet(DrawioImageSnippetViewSetGroup)


@hooks.register("register_icons")
def register_icons(icons):
    """register icons in the list of wagtail accessible icons"""
    return icons + [
        "wagtail_drawio/admin/icons/drawio.svg",
    ]
