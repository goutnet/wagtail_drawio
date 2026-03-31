from django.db import models

from wagtail.models import Page

from wagtail import blocks, fields
from wagtail.admin import panels

from wagtail_drawio.blocks import DrawIOImageChooserBlock


class HomePage(Page):
    """Home page model"""

    body = fields.StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
            # ("drawio_image", DrawIOImageBlock()),
            ("drawio_chooser", DrawIOImageChooserBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [panels.FieldPanel("body")]
