import pytest
from wagtail_drawio.blocks import DrawIOImageChooserBlock
from wagtail_drawio.models import DrawioImage

# A minimal valid PNG base64 string
SAMPLE_PNG_BASE64 = "iVBORw0KGgoAAAAADAAAAAQAAADAAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
SAMPLE_DIAGRAM_DATA = f"data:image/png;base64,{SAMPLE_PNG_BASE64}"


@pytest.mark.django_db
def test_drawio_image_chooser_block_instantiation():
    block = DrawIOImageChooserBlock()
    assert isinstance(block, DrawIOImageChooserBlock)


@pytest.mark.django_db
def test_drawio_image_chooser_block_value():
    image = DrawioImage.objects.create(
        title="Test Diagram",
        diagram=SAMPLE_DIAGRAM_DATA,
        width=1,
        height=1,
    )
    block = DrawIOImageChooserBlock()
    # The value of a SnippetChooserBlock is the snippet instance itself
    assert block.to_python(image.pk) == image
    assert block.get_prep_value(image) == image.pk


@pytest.mark.django_db
def test_drawio_image_chooser_block_render():
    image = DrawioImage.objects.create(
        title="Test Diagram",
        diagram=SAMPLE_DIAGRAM_DATA,
        width=100,
        height=50,
    )
    block = DrawIOImageChooserBlock()
    # When rendering a block, the value passed is the actual object
    html = block.render(image)
    assert f'src="/drawio/drawio-image/{image.pk}/"' in html
    assert f'alt="{image.title}"' in html
    assert f'title="{image.title}"' in html
    assert f'width="{image.width}"' in html
    assert f'height="{image.height}"' in html
    assert 'class="drawio_image"' in html


@pytest.mark.django_db
def test_drawio_image_block_does_not_leak_diagram_xml():
    """Verify that the block renders an img URL, not the raw diagram data (XML leak prevention)."""
    image = DrawioImage.objects.create(
        title="Sensitive Diagram",
        diagram=SAMPLE_DIAGRAM_DATA,
        width=100,
        height=50,
    )
    block = DrawIOImageChooserBlock()
    html = block.render(image)
    # The raw diagram data (base64 PNG with embedded XML) must NOT appear in the rendered HTML
    assert SAMPLE_PNG_BASE64 not in html
    assert SAMPLE_DIAGRAM_DATA not in html
    # Only a reference URL should be present
    assert f"/drawio/drawio-image/{image.pk}/" in html
