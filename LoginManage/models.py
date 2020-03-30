from django.db import models
from shortuuidfield import ShortUUIDField


class User(models.Model):
    id = ShortUUIDField(primary_key=True)
    username = models.CharField(max_length=254, unique=True)
    password = models.CharField(max_length=254)
    activated = models.BooleanField(default=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    nickname = models.CharField(max_length=254)
    create_time = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)

    department = models.ForeignKey('DeptManage.Department', null=True, default=None, on_delete=models.SET_DEFAULT)

    jurisdiction = models.ManyToManyField('JurisdictionManage.Jurisdiction', related_name='u_jurisdictions')

    class Meta:
        db_table = 'user'
        ordering = ['-create_time']
