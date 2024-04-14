# Generated by Django 5.0.4 on 2024-04-14 00:18

import wagtail.blocks
import wagtail.fields
import wagtail.snippets.blocks
import wagtail_drawio.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_create_homepage"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("paragraph", wagtail.blocks.RichTextBlock()),
                    (
                        "drawio_image",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "diagram",
                                    wagtail.snippets.blocks.SnippetChooserBlock(
                                        wagtail_drawio.models.DrawioImage,
                                        help_text="diagram",
                                    ),
                                ),
                                (
                                    "width",
                                    wagtail.blocks.IntegerBlock(
                                        blank=True,
                                        default=0,
                                        help_text="Width of the diagram (null use diagram width)",
                                        null=True,
                                    ),
                                ),
                                (
                                    "height",
                                    wagtail.blocks.IntegerBlock(
                                        blank=True,
                                        default=0,
                                        help_text="Height of the diagram (null use diagram height)",
                                        null=True,
                                    ),
                                ),
                            ]
                        ),
                    ),
                ],
                blank=True,
                null=True,
            ),
        ),
    ]