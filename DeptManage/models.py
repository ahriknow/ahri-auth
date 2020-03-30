from django.db import models
from shortuuidfield import ShortUUIDField


class Department(models.Model):
    id = ShortUUIDField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    describe = models.TextField(default='')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True, null=True)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True)

    jurisdiction = models.ManyToManyField('JurisdictionManage.Jurisdiction', related_name='d_jurisdictions')

    class Meta:
        db_table = 'department'
