"""
API Hooks for Wagtail
Adding edit pages for images

This code is distributed under the MIT License
"""

from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

# from wagtail.admin.menu import MenuItem

from .models import DrawioImage


class DrawioImageSnippetViewSet(SnippetViewSet):
    """Adding edition of Drawio image models"""

    model = DrawioImage

    menu_label = "Drawio Images"
    icon = "drawio"

    list_display = ("pk", "title", "created_at")


register_snippet(DrawioImageSnippetViewSet)


@hooks.register("register_icons")
def register_icons(icons):
    """register icons in the list of wagtail accessible icons"""
    return icons + [
        "wagtail_drawio/admin/icons/drawio.svg",
    ]
