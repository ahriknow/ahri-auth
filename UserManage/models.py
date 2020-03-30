from django.db import models
from shortuuidfield import ShortUUIDField


class UserInfo(models.Model):
    id = ShortUUIDField(primary_key=True)
    name = models.CharField(max_length=254, default='')

    user = models.OneToOneField('LoginManage.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_info'
