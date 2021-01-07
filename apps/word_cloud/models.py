import time

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models

upload_storage = FileSystemStorage(location=settings.STATIC_ROOT, base_url="/static")


def image_upload_to(instance, filename):
    unix_ts = int(time.time())
    return f"images/{unix_ts}_{filename}.jpeg"


class WordCloud(models.Model):
    keyword = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default=None,
        help_text="Keyword that was sent in request",
    )
    related_words = models.TextField(
        null=True, blank=True, default=None, help_text="Words related to keyword",
    )
    image = models.ImageField(
        max_length=1024,
        upload_to=image_upload_to,
        storage=upload_storage,
        null=True,
        blank=True,
        help_text="The image that was created based on keyword and related words",
    )

    def __str__(self):
        return f"Word Cloud for keyword: {self.keyword}"
