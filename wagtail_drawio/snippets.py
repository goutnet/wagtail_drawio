"""
Snippets for Drawio image models

This code is distributed under the MIT License.
"""

from wagtail.snippets.views.snippets import SnippetViewSet

from .models import DrawioImage


class DrawioImageSnippetViewSet(SnippetViewSet):
    """Adding edition of Drawio image models"""

    _placeholder = None

    model = DrawioImage

    menu_label = "Drawio Diagrams"
    icon = "drawio"

    list_display = ("pk", "title", "preview", "created_at", "tags_list")
    list_filter = ("title", "created_at")
