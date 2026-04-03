import pytest
from django.urls import reverse
from wagtail_drawio.models import DrawioImage
import base64
from unittest.mock import patch, MagicMock
import png  # Import png to mock it

# A minimal valid PNG base64 string
SAMPLE_PNG_BASE64 = "iVBORw0KGgoAAAAADAAAAAQAAADAAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
SAMPLE_DIAGRAM_DATA = f"data:image/png;base64,{SAMPLE_PNG_BASE64}"


@pytest.mark.django_db
@patch("png.Reader")
def test_drawio_image_view(mock_png_reader, client):
    mock_reader_instance = MagicMock()
    mock_png_reader.return_value = mock_reader_instance
    mock_reader_instance.chunks.return_value = [
        (b"IHDR", b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00"),
        (
            b"IDAT",
            b"\x78\x9c\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00\x00\x00\x00\x00",
        ),
        (b"IEND", b""),
    ]

    image = DrawioImage.objects.create(
        title="Test Diagram",
        diagram=SAMPLE_DIAGRAM_DATA,
        width=1,
        height=1,
    )
    url = reverse("wagtail_drawio:drawio_image", args=[image.pk])
    response = client.get(url)

    assert response.status_code == 200
    assert response["Content-Type"] == "image/png"
    # The content should be a valid PNG, but not necessarily the original SAMPLE_PNG_BASE64
    # because png_as_image re-encodes it. We'll check if it's bytes and not empty.
    assert isinstance(response.content, bytes)
    assert len(response.content) > 0
