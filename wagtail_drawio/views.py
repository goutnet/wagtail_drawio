"""
DrawIO views
This code is distributed under the MIT License
"""

from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from wagtail.admin.viewsets.chooser import ChooserViewSet

from .models import DrawioImage


def drawio_image(request, image_id):  # pylint: disable=unused-argument
    """Returns the PNG content of a DrawIO image"""
    image = DrawioImage.objects.get(pk=image_id)
    return HttpResponse(image.as_png_image(), content_type="image/png")


class DrawioChooserViewSet(ChooserViewSet):
    """
    Viewset for choosing a DrawIO diagram (used to provide a create tab)
    """

    # The model can be specified as either the model class or an "app_label.model_name" string;
    # using a string avoids circular imports when accessing the StreamField block class (see below)
    model = "wagtail_drawio.DrawioImage"

    add_to_admin_menu = True

    icon = "drawio"

    choose_one_text = _("Choose a diagram")
    choose_another_text = _("Choose another diagram")
    edit_item_text = _("Edit this diagram")

    form_fields = "__all__"


drawio_chooser_viewset = DrawioChooserViewSet("drawio_chooser")
