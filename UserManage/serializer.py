from rest_framework import serializers
from LoginManage.models import User
from UserManage.models import UserInfo


class OneUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'email', 'phone', 'create_time', 'activated', 'jurisdiction',
                  'last_login']


class ManyUser(serializers.ModelSerializer):
    userinfo = serializers.SerializerMethodField()

    def get_userinfo(self, row):
        return OneUserinfo(instance=row.userinfo, many=False).data

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'email', 'phone', 'create_time', 'last_login', 'jurisdiction',
                  'department', 'activated', 'userinfo']


class LoginInfo(serializers.ModelSerializer):
    userinfo = serializers.SerializerMethodField()

    def get_userinfo(self, row):
        return OneUserinfo(instance=row.userinfo, many=False).data

    class Meta:
        model = User
        fields = ['username', 'nickname', 'email', 'phone', 'create_time', 'last_login', 'activated', 'userinfo']


class OneUserinfo(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = "__all__"
