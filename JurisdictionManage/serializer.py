from rest_framework import serializers
from JurisdictionManage.models import Jurisdiction


class OneJurisdiction(serializers.ModelSerializer):
    class Meta:
        model = Jurisdiction
        fields = "__all__"


class ManyJurisdiction(serializers.ModelSerializer):
    class Meta:
        model = Jurisdiction
        fields = "__all__"


class ManyJurisdictionId(serializers.ModelSerializer):
    class Meta:
        model = Jurisdiction
        fields = ['identification']
