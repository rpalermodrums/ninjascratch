from uuid import uuid4

from django.db import models

# Create your models here.
class AbstractTimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractBaseModel(AbstractTimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4)

    class Meta:
        abstract = True


class Address(models.Model):
    address1 = models.CharField(max_length=128)
    address2 = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=5)

    class Meta:
        db_table = 'addresses'
        verbose_name_plural = 'addresses'
        ordering = ('zip', )
