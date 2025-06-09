import uuid

from django.db import models


class TimeStampedMixin(models.Model):
    """Добавляет время создания и обновления."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Метакласс."""

        abstract = True


class TimeStampedCreatedMixin(models.Model):
    """Добавляет время создания."""

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Метакласс."""

        abstract = True


class UUIDMixin(models.Model):
    """Добавляет uuid."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    class Meta:
        """Метакласс."""

        abstract = True
