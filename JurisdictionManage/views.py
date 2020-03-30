from rest_framework.response import Response
from rest_framework.views import APIView
from JurisdictionManage.models import Jurisdiction
from JurisdictionManage.serializer import OneJurisdiction, ManyJurisdiction


class JurManageView(APIView):
    def get(self, request, id=None):
        if id:
            if jur := Jurisdiction.objects.filter(pk=id).first():
                data = OneJurisdiction(instance=jur, many=False).data
                return Response({'code': 200, 'msg': 'Query was successful!', 'data': data})
            return Response({'code': 400, 'msg': 'Data does not exist!', 'data': None})
        else:
            jurs = Jurisdiction.objects.all()
            data = ManyJurisdiction(instance=jurs, many=True).data
            return Response({'code': 200, 'msg': 'Query was successful!', 'data': data})

    def post(self, request):
        try:
            jur = Jurisdiction(name=request.data['name'], describe=request.data['describe'],
                               identification=request.data['identification'])
            jur.save()
            return Response({'code': 200, 'msg': 'Create successful!', 'data': None})
        except Exception as ex:
            if 'UNIQUE' in str(ex):
                return Response({'code': 400, 'msg': 'Data duplication!', 'data': None})
            return Response({'code': 500, 'msg': str(ex), 'data': None})

    def put(self, request, id=None):
        if jur := Jurisdiction.objects.filter(pk=id).first():
            data = request.data
            if name := data.get('name'):
                jur.name = name
            if describe := data.get('describe'):
                jur.describe = describe
            if identification := data.get('identification'):
                jur.identification = identification
            jur.save()
            return Response({'code': 200, 'msg': 'Update successful!', 'data': None})
        return Response({'code': 400, 'msg': 'Data does not exist!', 'data': None})

    def delete(self, request, id=None):
        if jur := Jurisdiction.objects.filter(pk=id).first():
            jur.delete()
            return Response({'code': 200, 'msg': 'Delete successful!'})
        return Response({'code': 400, 'msg': 'Data does not exist!', 'data': None})
