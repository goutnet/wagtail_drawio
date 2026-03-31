"""
API Hooks for Wagtail
Adding edit pages for images

This code is distributed under the MIT License
"""

from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSetGroup

from .snippets import DrawioImageSnippetViewSet
from .views import drawio_chooser_viewset


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


@hooks.register("register_admin_viewset")
def register_drawio_chooser_viewset():
    """register the Drawio chooser viewset"""
    return drawio_chooser_viewset
