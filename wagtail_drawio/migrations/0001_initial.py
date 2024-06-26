# Generated by Django 5.0.4 on 2024-04-13 20:27

import django.db.models.deletion
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DrawioImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(help_text="Title of the diagram", max_length=255),
                ),
                (
                    "diagram",
                    models.TextField(
                        blank=True, help_text="DrawIO diagram (double click to edit)"
                    ),
                ),
                (
                    "width",
                    models.IntegerField(
                        default=0, help_text="Width of the diagram (auto filled)"
                    ),
                ),
                (
                    "height",
                    models.IntegerField(
                        default=0, help_text="Height of the diagram (auto filled)"
                    ),
                ),
                (
                    "xml_content",
                    models.TextField(
                        blank=True, help_text="XML diagram content", null=True
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="created at"
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text=None,
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="tags",
                    ),
                ),
                (
                    "uploaded_by_user",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="uploaded by user",
                    ),
                ),
            ],
            options={
                "verbose_name": "DrawIO diagram",
                "verbose_name_plural": "DrawIO diagrams",
                "permissions": [("choose_diagram", "Can choose a DrawIO diagram")],
            },
        ),
    ]
