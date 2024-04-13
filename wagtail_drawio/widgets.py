"""
Custom Widget allowing the edition of the DrawIO diagram content

This code is distributed under the MIT License, see the LICENSE file
"""

from django import forms


class DrawioWidget(forms.Textarea):
    """ensure the widget used override the default Textarea widget"""

    template_name = "wagtail_drawio/widgets/drawio_widget.html"
