from rest_framework.response import Response
from rest_framework.views import APIView
from DeptManage.models import Department
from DeptManage.serializer import OneDepartment, ManyDepartment
from JurisdictionManage.models import Jurisdiction


class DeptManageView(APIView):
    def get(self, request, id=None):
        if id:
            if dept := Department.objects.filter(pk=id).first():
                data = OneDepartment(instance=dept, many=False).data
                return Response({'code': 200, 'msg': 'Query was successful!', 'data': data})
            return Response({'code': 400, 'msg': 'Data does not exist!', 'data': None})
        else:
            depts = Department.objects.all()
            data = ManyDepartment(instance=depts, many=True).data
            return Response({'code': 200, 'msg': 'Query was successful!', 'data': data})

    def post(self, request):
        try:
            dept = Department(name=request.data['name'], describe=request.data['describe'])
            if request.data['parent']:
                if parent := Department.objects.filter(pk=request.data['parent']).first():
                    dept.parent = parent
                else:
                    return Response({'code': 400, 'msg': "The 'parent' does not exist!", 'data': None})
            dept.save()
            return Response({'code': 200, 'msg': 'Create successful!', 'data': None})
        except Exception as ex:
            if 'UNIQUE' in str(ex):
                return Response({'code': 400, 'msg': 'Data duplication!', 'data': None})
            return Response({'code': 500, 'msg': str(ex), 'data': None})

    def put(self, request, id=None):
        if dept := Department.objects.filter(pk=id).first():
            data = request.data
            if name := data.get('name'):
                dept.name = name
            if describe := data.get('describe'):
                dept.describe = describe
            if parent := data.get('parent'):
                dept.parent = parent
            if 'jurisdiction' in data:
                dept.jurisdiction.clear()
                if jurisdiction := data['jurisdiction']:
                    jurs = Jurisdiction.objects.filter(pk__in=jurisdiction)
                    for i in jurs:
                        dept.jurisdiction.add(i)
            dept.save()
            return Response({'code': 200, 'msg': 'Update successful!', 'data': None})
        return Response({'code': 400, 'msg': 'Data does not exist!', 'data': None})

    def delete(self, request, id=None):
        if dept := Department.objects.filter(pk=id).first():
            dept.delete()
            return Response({'code': 200, 'msg': 'Delete successful!'})
        return Response({'code': 400, 'msg': 'Data does not exist!', 'data': None})
