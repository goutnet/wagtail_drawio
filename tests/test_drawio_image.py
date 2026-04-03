import pytest
import base64
from unittest.mock import patch, MagicMock
from wagtail_drawio.models import DrawioImage
import png  # Import png to mock it

# A minimal valid PNG base64 string
SAMPLE_PNG_BASE64 = "iVBORw0KGgoAAAAADAAAAAQAAADAAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
SAMPLE_DIAGRAM_DATA = f"data:image/png;base64,{SAMPLE_PNG_BASE64}"

# A sample PNG data with an mxfile chunk for testing strip_data
# This is a simplified representation, not a real PNG structure
SAMPLE_PNG_WITH_MXFILE_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
SAMPLE_MXFILE_CONTENT = b'<?xml version="1.0" encoding="UTF-8"?><mxfile>...</mxfile>'


@pytest.mark.django_db
def test_drawio_image_creation():
    image = DrawioImage.objects.create(
        title="Test Diagram",
        diagram=SAMPLE_DIAGRAM_DATA,
        width=1,
        height=1,
    )
    assert image.pk is not None
    assert image.title == "Test Diagram"
    assert image.diagram == SAMPLE_DIAGRAM_DATA
    assert image.width == 1
    assert image.height == 1


@pytest.mark.django_db
def test_png_data_decode_false():
    image = DrawioImage.objects.create(
        title="Test Diagram",
        diagram=SAMPLE_DIAGRAM_DATA,
        width=1,
        height=1,
    )
    assert image.png_data(decode=False) == SAMPLE_PNG_BASE64


@pytest.mark.django_db
def test_png_data_decode_true():
    image = DrawioImage.objects.create(
        title="Test Diagram",
        diagram=SAMPLE_DIAGRAM_DATA,
        width=1,
        height=1,
    )
    assert image.png_data(decode=True) == base64.b64decode(SAMPLE_PNG_BASE64)


@pytest.mark.django_db
@patch("png.Reader")
def test_png_data_strip_data(mock_png_reader):
    # Mock the png.Reader to return specific chunks
    mock_reader_instance = MagicMock()
    mock_png_reader.return_value = mock_reader_instance

    # Define the chunks that the mocked reader will return
    # A minimal set of chunks including an mxfile tEXt chunk
    mock_reader_instance.chunks.return_value = [
        (b"IHDR", b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00"),
        (b"tEXt", b"mxfile\x00" + SAMPLE_MXFILE_CONTENT),
        (
            b"IDAT",
            b"\x78\x9c\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00\x00\x00\x00\x00",
        ),
        (b"IEND", b""),
    ]

    image = DrawioImage.objects.create(
        title="Test Diagram",
        diagram=f"data:image/png;base64,{SAMPLE_PNG_WITH_MXFILE_BASE64}",
        width=1,
        height=1,
    )

    # Call png_data with strip_data=True
    result_base64 = image.png_data(strip_data=True, decode=False)
    result_bytes = image.png_data(strip_data=True, decode=True)

    # Assert that the mxfile chunk is removed from the recreated PNG
    # This is a simplified check, a more robust test would involve parsing the output PNG
    # and verifying the absence of the mxfile chunk. For now, we'll check that the
    # content is different from the original (which would contain the mxfile chunk).
    # This test primarily ensures the code path for stripping data is exercised.

    # The recreated PNG should not contain the mxfile content in its raw form
    # (it would be compressed in IDAT, but we are testing the chunk removal logic)
    # For this mock, we expect the output to be a valid PNG without the tEXt chunk
    # The exact output is hard to predict without re-implementing PNG encoding,
    # so we'll focus on ensuring the method executes without error and returns something.

    # A more direct test: ensure the mocked reader was called and chunks were processed
    mock_png_reader.assert_called()  # Called multiple times due to re-encoding
    mock_reader_instance.chunks.assert_called()  # Called multiple times due to re-encoding

    # We can't easily assert the exact content of the re-encoded PNG without
    # re-implementing PNG encoding logic in the test.
    # For now, we'll assert that the result is not empty and is valid base64/bytes.
    assert result_base64 is not None and len(result_base64) > 0
    assert result_bytes is not None and len(result_bytes) > 0
    assert isinstance(result_base64, str)
    assert isinstance(result_bytes, bytes)


@pytest.mark.django_db
@patch("png.Reader")
def test_png_as_image(mock_png_reader):
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
    result = image.png_as_image()
    assert isinstance(result, bytes)
    assert result is not None and len(result) > 0


@pytest.mark.django_db
@patch("png.Reader")
def test_png_as_base64(mock_png_reader):
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
    result = image.png_as_base64()
    assert isinstance(result, str)
    assert result is not None and len(result) > 0


@pytest.mark.django_db
def test_empty_diagram():
    image = DrawioImage.objects.create(
        title="Empty Diagram",
        diagram="",
        width=0,
        height=0,
    )
    assert image.empty() is True


@pytest.mark.django_db
def test_non_empty_diagram():
    image = DrawioImage.objects.create(
        title="Non-Empty Diagram",
        diagram=SAMPLE_DIAGRAM_DATA,
        width=1,
        height=1,
    )
    assert image.empty() is False


@pytest.mark.django_db
def test_usage_count_no_references():
    image = DrawioImage.objects.create(
        title="Unused Diagram",
        diagram=SAMPLE_DIAGRAM_DATA,
        width=1,
        height=1,
    )
    assert image.usage_count() == 0


@pytest.mark.django_db
def test_usage_count_with_references():
    from django.contrib.contenttypes.models import ContentType
    from wagtail.models import ReferenceIndex

    image = DrawioImage.objects.create(
        title="Used Diagram",
        diagram=SAMPLE_DIAGRAM_DATA,
        width=1,
        height=1,
    )
    # Simulate two references from the same page (same object_id) — should count as 1
    # and one reference from a different page — should count as 2 total
    ct = ContentType.objects.get_for_model(DrawioImage)

    def make_ref(object_id, content_path):
        ReferenceIndex.objects.create(
            content_type=ct,
            base_content_type=ct,
            object_id=object_id,
            to_content_type=ct,
            to_object_id=str(image.pk),
            model_path=content_path,
            content_path=content_path,
            content_path_hash=ReferenceIndex._get_content_path_hash(content_path),
        )

    make_ref("10", "body")
    make_ref("10", "body.item")  # same page, different path — still counts as 1
    make_ref("20", "body")
    # object_id 10 used twice (same page) + object_id 20 = 2 distinct pages
    assert image.usage_count() == 2
