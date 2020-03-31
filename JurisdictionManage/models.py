from django.db import models
from shortuuidfield import ShortUUIDField


class Jurisdiction(models.Model):
    id = ShortUUIDField(primary_key=True)
    name = models.CharField(max_length=254, unique=True)
    describe = models.TextField(default='')
    identification = models.CharField(max_length=254, unique=True)

    class Meta:
        ordering = ['name']
        db_table = 'jurisdiction'
