"""
Wagtail DrawIO Block
This code is distributed under the MIT License, see the LICENSE file
"""

from django.utils.translation import gettext_lazy as _

from wagtail import blocks
from wagtail.snippets.blocks import SnippetChooserBlock

from .models import DrawioImage


class DrawIOImageBlock(blocks.StructBlock):  # pylint: disable=too-few-public-methods
    """
    DrawIO Image Block
    This block allows to either select an existing DrawIO object,
    or make a new one in the editor.

    Display template only show the image, not the drawIO representation.
    """

    diagram = SnippetChooserBlock(DrawioImage, help_text=_("diagram"))

    class Meta:  # pylint: disable=too-few-public-methods
        icon = "drawio"
        label = _("DrawIO Diagram")

        template = "wagtail_drawio/blocks/drawio_image_block.html"
