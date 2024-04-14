"""
Custom Widget allowing the edition of the DrawIO diagram content

This code is distributed under the MIT License, see the LICENSE file
"""

from django import forms
from django.utils.html import mark_safe

from .settings import drawio_url


class DrawioWidget(forms.Textarea):
    """ensure the widget used override the default Textarea widget"""

    template_name = "wagtail_drawio/widgets/drawio_widget.html"

    @property
    def media(self):
        """add the required media for the widget"""
        return forms.Media(
            css={"all": ("css/drawio_widget.css",)},
            js=("js/drawio_widget.js",),
        )

    def get_context(self, name, value, attrs):
        """add the drawio_url to the context"""
        context = super().get_context(name, value, attrs)
        context["drawio_url"] = mark_safe(drawio_url)
        return context
