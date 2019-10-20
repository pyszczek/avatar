import os
import uuid

from django.conf import settings
from django.utils.crypto import get_random_string

SECRET_KEY = settings.SECRET_KEY


def generate_uuid():
    return uuid.uuid4()
