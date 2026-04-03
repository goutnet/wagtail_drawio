import pytest
from unittest.mock import MagicMock, patch
from django.test import RequestFactory
from wagtail_drawio.models import DrawioImage
from wagtail_drawio.panels import DrawioUsagePanel

SAMPLE_PNG_BASE64 = "iVBORw0KGgoAAAAADAAAAAQAAADAAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
SAMPLE_DIAGRAM_DATA = f"data:image/png;base64,{SAMPLE_PNG_BASE64}"


@pytest.mark.django_db
def test_usage_panel_no_references():
    image = DrawioImage.objects.create(
        title="Unused",
        diagram=SAMPLE_DIAGRAM_DATA,
        width=1,
        height=1,
    )
    panel = DrawioUsagePanel()
    request = MagicMock()
    bound = panel.bind_to_model(DrawioImage).get_bound_panel(
        instance=image, request=request, form=None, prefix="panel"
    )
    context = bound.get_context_data()
    assert context["usages"] == []


@pytest.mark.django_db
def test_usage_panel_with_references():
    from django.contrib.contenttypes.models import ContentType
    from wagtail.models import ReferenceIndex

    image = DrawioImage.objects.create(
        title="Used",
        diagram=SAMPLE_DIAGRAM_DATA,
        width=1,
        height=1,
    )
    ct = ContentType.objects.get_for_model(DrawioImage)
    ReferenceIndex.objects.create(
        content_type=ct,
        base_content_type=ct,
        object_id=str(image.pk),
        to_content_type=ct,
        to_object_id=str(image.pk),
        model_path="body",
        content_path="body",
        content_path_hash=ReferenceIndex._get_content_path_hash("body"),
    )

    panel = DrawioUsagePanel()
    request = MagicMock()

    with patch(
        "wagtail.admin.admin_url_finder.AdminURLFinder.get_edit_url",
        return_value="/admin/snippets/wagtail_drawio/drawioimage/1/edit/",
    ):
        bound = panel.bind_to_model(DrawioImage).get_bound_panel(
            instance=image, request=request, form=None, prefix="panel"
        )
        context = bound.get_context_data()

    assert len(context["usages"]) == 1
    assert context["usages"][0]["label"] == str(image)
    assert (
        context["usages"][0]["edit_url"]
        == "/admin/snippets/wagtail_drawio/drawioimage/1/edit/"
    )


@pytest.mark.django_db
def test_usage_panel_unsaved_instance_returns_empty():
    """Panel on the create form (unsaved instance) should return empty usages."""
    image = DrawioImage(title="New", diagram=SAMPLE_DIAGRAM_DATA, width=1, height=1)
    panel = DrawioUsagePanel()
    request = MagicMock()
    bound = panel.bind_to_model(DrawioImage).get_bound_panel(
        instance=image, request=request, form=None, prefix="panel"
    )
    context = bound.get_context_data()
    assert context["usages"] == []


@pytest.mark.django_db
def test_usage_panel_renders_edit_link():
    """Rendered HTML must contain the edit link — catches template variable scope bugs."""
    from django.contrib.contenttypes.models import ContentType
    from wagtail.models import ReferenceIndex

    image = DrawioImage.objects.create(
        title="Diagram A", diagram=SAMPLE_DIAGRAM_DATA, width=1, height=1
    )
    ct = ContentType.objects.get_for_model(DrawioImage)
    ReferenceIndex.objects.create(
        content_type=ct,
        base_content_type=ct,
        object_id=str(image.pk),
        to_content_type=ct,
        to_object_id=str(image.pk),
        model_path="body",
        content_path="body",
        content_path_hash=ReferenceIndex._get_content_path_hash("body"),
    )

    panel = DrawioUsagePanel()
    request = RequestFactory().get("/")
    request.user = MagicMock()

    edit_url = f"/admin/snippets/wagtail_drawio/drawioimage/{image.pk}/edit/"
    with patch(
        "wagtail.admin.admin_url_finder.AdminURLFinder.get_edit_url",
        return_value=edit_url,
    ):
        bound = panel.bind_to_model(DrawioImage).get_bound_panel(
            instance=image, request=request, form=None, prefix="panel"
        )
        html = bound.render_html()

    assert edit_url in html
    assert str(image) in html
    assert "Not used anywhere" not in html


@pytest.mark.django_db
def test_usage_panel_renders_not_used_when_empty():
    """Rendered HTML shows 'Not used anywhere' when there are no references."""
    image = DrawioImage.objects.create(
        title="Lonely Diagram", diagram=SAMPLE_DIAGRAM_DATA, width=1, height=1
    )
    panel = DrawioUsagePanel()
    request = RequestFactory().get("/")
    request.user = MagicMock()
    bound = panel.bind_to_model(DrawioImage).get_bound_panel(
        instance=image, request=request, form=None, prefix="panel"
    )
    html = bound.render_html()
    assert "Not used anywhere" in html
