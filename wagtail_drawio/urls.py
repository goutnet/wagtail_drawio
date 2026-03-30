from django.urls import path

from . import views

app_name = "wagtail_drawio"

urlpatterns = [
    path("drawio-image/<int:image_id>/", views.drawio_image, name="drawio_image"),
]
