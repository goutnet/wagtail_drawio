"""
Wagtail DrawIO Block Models
This code is distributed under the MIT License, see the LICENSE file
"""

import base64
import zlib
import os

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe

from taggit.managers import TaggableManager

from wagtail.admin import panels
from .widgets import DrawioWidget


class DrawioImage(models.Model):
    """
    DrawIO Image model, holds the image and its metadata
    diagram contains a string representation of the image, in the following format:
    data:image/png;base64,IMAGE_DATA

    the drawIO diagram is actually stored in the compressed text section of the PNG

    - https://www.drawio.com/blog/embedding-walkthrough
    - https://www.drawio.com/doc/faq/embed-mode

    The rationale behind having a model is to allow blocks to refer to the same
    image, and to allow for a more flexible storage of the image data. This means
    an image can reference multiple blocks, updating the image in one place will
    update it everywhere.
    """

    _placeholder = None

    title = models.CharField(max_length=255, help_text=_("Title of the diagram"))

    diagram = models.TextField(
        blank=True, help_text=_("DrawIO diagram (double click to edit)")
    )

    width = models.IntegerField(
        default=0, help_text=_("Width of the diagram (auto filled)")
    )
    height = models.IntegerField(
        default=0, help_text=_("Height of the diagram (auto filled)")
    )
    xml_content = models.TextField(
        help_text=_("XML diagram content"), blank=True, null=True
    )

    tags = TaggableManager(help_text=None, blank=True, verbose_name=_("tags"))
    created_at = models.DateTimeField(
        verbose_name=_("created at"), auto_now_add=True, db_index=True
    )

    uploaded_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("uploaded by user"),
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
    )
    uploaded_by_user.wagtail_reference_index_ignore = True

    def png_content(self, strip_data=False, decode=False):
        """
        Returns the PNG content of the image.
        if strip_data the compressed text section is removed
        """
        b64_content = self.diagram.split(",", 1)[1]

        if decode or strip_data:
            data = base64.b64decode(b64_content)
            # To be verified:
            # The compressed text section is the last section of the PNG
            # (IHDR, PLTE, IDAT, IEND)
            if strip_data:
                try:
                    decompress = zlib.decompress(data, 15)
                    if decode:
                        return decompress
                    return base64.b64encode(decompress)

                except zlib.error:
                    # likely not compressed data there
                    print("DEBUG: zlib error, no compress data?")

            return data
        return b64_content

    @staticmethod
    def placeholder():
        """return the base64 encoded placeholder image"""
        if DrawioImage._placeholder is None:
            path = os.path.join(
                os.path.dirname(__file__), "static/admin/media/drawio_edit.svg"
            )

            with open(path, "rb", encoding="utf8") as f:
                content = base64.b64encode(f.read())
            DrawioImage._placeholder = f"data:image/svg;base64,{content}"

    def preview(self):
        """Returns a list preview tag of the diagram"""
        content = self.diagram
        if self.empty():
            content = self.placeholder()
        return mark_safe(f'<img src="{content}" alt="{self.title}" width="100px"/>')

    def tags_list(self):
        """Returns a list of tags"""
        return ", ".join(self.tags.names())

    def png_image(self):
        """shortcut to png_content"""
        return self.png_content(decode=True, strip_data=True)

    def png_base64(self):
        """shortcut to png_content"""
        return self.png_content(decode=False, strip_data=True)

    def empty(self):
        """
        Returns True if the image is empty, False otherwise
        """
        return not self.diagram

    class Meta:
        verbose_name = _("DrawIO Diagram")
        verbose_name_plural = _("DrawIO Diagrams")
        permissions = [
            ("choose_diagram", "Can choose a DrawIO diagram"),
        ]

    panels = [
        panels.FieldPanel("title", icon="title"),
        panels.FieldPanel("diagram", icon="drawio", widget=DrawioWidget),
        panels.FieldPanel("tags"),
        panels.FieldRowPanel(
            (
                panels.FieldPanel("width"),
                panels.FieldPanel("height"),
            )
        ),
        panels.FieldPanel("xml_content", classname="collapsed", icon="code"),
    ]
