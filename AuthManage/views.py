from rest_framework.response import Response
from rest_framework.views import APIView
from JurisdictionManage.serializer import ManyJurisdictionId
from LoginManage.models import User


class AuthManageView(APIView):
    def get(self, request, id=None):
        if user := User.objects.filter(pk=id).first():
            result = ManyJurisdictionId(instance=user.department.jurisdiction, many=True).data
            user_jurs = ManyJurisdictionId(instance=user.jurisdiction, many=True).data
            data = list()
            for i in result:
                data.append(i['identification'])
            for i in user_jurs:
                if i['identification'] not in data:
                    data.append(i['identification'])
            return Response({'code': 200, 'msg': 'Query was successful!', 'data': data})
        return Response({'code': 400, 'msg': 'Data does not exist!', 'data': None})

    def post(self, request):
        try:
            if user := User.objects.filter(pk=request.data.get('token')).first():
                result = ManyJurisdictionId(instance=user.department.jurisdiction, many=True).data
                user_jurs = ManyJurisdictionId(instance=user.jurisdiction, many=True).data
                data = list()
                for i in result:
                    data.append(i['identification'])
                for i in user_jurs:
                    if i['identification'] not in data:
                        data.append(i['identification'])
                return Response({'code': 200, 'msg': 'Query was successful!', 'data': data})
            return Response({'code': 400, 'msg': 'Data does not exist!', 'data': None})
        except Exception as ex:
            return Response({'code': 500, 'msg': str(ex), 'data': None})
