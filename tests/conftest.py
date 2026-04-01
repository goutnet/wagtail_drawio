import django
from django.conf import settings


def pytest_configure():
    if not settings.configured:
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wagtail_drawio.test_settings')
        django.setup()
