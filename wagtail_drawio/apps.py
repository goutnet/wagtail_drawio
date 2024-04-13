"""
DrawIO app configuration
(mainly removing some wagtail warnings)

This code is licensed under the MIT license. See the LICENSE file in the root
"""

from django.apps import AppConfig


class DrawIOAppConfig(AppConfig):
    """Meta data for the DrawIO app"""

    name = "wagtail_drawio"
    label = "wagtail_drawio"
    verbose_name = "DrawIO"

    default_auto_field = "django.db.models.AutoField"
