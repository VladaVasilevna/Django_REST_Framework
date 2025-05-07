from urllib.parse import urlparse

from rest_framework import serializers


def validate_video_url(value):
    """Проверяет, что ссылка относится к youtube.com."""
    parsed_url = urlparse(value)
    if parsed_url.netloc.lower() not in ["www.youtube.com", "youtube.com"]:
        raise serializers.ValidationError("Ссылка должна быть на youtube.com")
