import django
import os
import pytest
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itec2025.settings')
django.setup()

from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

