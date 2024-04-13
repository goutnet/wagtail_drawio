"""
Wagtail DrawIO Block
This code is distributed under the MIT License, see the LICENSE file
"""

from django.utils.translation import gettext_lazy as _
from django import forms

from wagtail.core import blocks
from wagtail.admin.forms.choosers import AdminChooser

from .models import DrawioImage


class DrawIOImageChooser(AdminChooser):  # pylint: disable=too-few-public-methods
    """
    Choose an existing DrawIO Image (or allow one to be created)
    """

    choose_one_text = _("Choose a DrawIO Image")
    model = DrawioImage


class DrawIOImageBlock(blocks.StructBlock):  # pylint: disable=too-few-public-methods
    """
    DrawIO Image Block
    This block allows to either select an existing DrawIO object,
    or make a new one in the editor.

    Display template only show the image, not the drawIO representation.
    """

    def __init__(self, required=True, help_text=None, **kwargs):
        self.field = forms.ModelChoiceField(
            queryset=DrawioImage.objects.all(),
            widget=DrawIOImageChooser,
            required=required,
            help_text=help_text,
        )

        super().__init__(**kwargs)

    image = blocks.ForeignKeyBlock(DrawIOImage, help_text=_("diagram"))
    # width = models.IntegerField(
    #     default=0, help_text="Width of the image in pixels, 0 if unknown"
    # )
    # height = models.IntegerField(
    #     default=0, help_text="Height of the image in pixels, 0 if unknown"
    # )
