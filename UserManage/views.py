from rest_framework.response import Response
from rest_framework.views import APIView
from DeptManage.models import Department
from JurisdictionManage.models import Jurisdiction
from LoginManage.models import User
from UserManage.models import UserInfo
from UserManage.serializer import OneUser, ManyUser


class UserManageView(APIView):
    def get(self, request, id=None):
        if id:
            if user := User.objects.filter(pk=id).first():
                data = OneUser(instance=user, many=False).data
                return Response({'code': 200, 'msg': 'Query was successful!', 'data': data})
            return Response({'code': 400, 'msg': 'Data does not exist!', 'data': None})
        else:
            users = User.objects.all()
            data = ManyUser(instance=users, many=True).data
            return Response({'code': 200, 'msg': 'Query was successful!', 'data': data})

    def post(self, request):
        try:
            user = User(username=request.data['username'],
                        password=request.data['password'],
                        email=request.data.get('email', ''),
                        phone=request.data.get('phone', ''),
                        nickname=request.data.get('nickname', ''))
            if department := request.data.get('department'):
                dept = Department.objects.filter(pk=department).first()
                if dept:
                    user.department = dept
            user.save()
            userinfo = UserInfo(user=user)
            if u := request.data.get('userinfo'):
                if name := u.get('name'):
                    userinfo.name = name
            userinfo.save()
            return Response({'code': 200, 'msg': 'Create successful!', 'data': None})
        except Exception as ex:
            if 'UNIQUE' in str(ex):
                return Response({'code': 400, 'msg': 'Data duplication!', 'data': None})
            return Response({'code': 500, 'msg': str(ex), 'data': None})

    def put(self, request, id=None):
        if user := User.objects.filter(pk=id).first():
            data = request.data
            if department := data.get('department'):
                dept = Department.objects.filter(pk=department).first()
                if dept:
                    user.department = dept
                else:
                    return Response({'code': 400, 'msg': "The 'department' does not exist!", 'data': None})
            if (activated := data.get('activated', '')) in [True, False]:
                user.activated = activated
            if username := data.get('username'):
                user.username = username
            if password := data.get('password'):
                user.password = password
            if email := data.get('email'):
                user.email = email
            if phone := data.get('phone'):
                user.phone = phone
            if nickname := data.get('nickname'):
                user.nickname = nickname
            if 'jurisdiction' in data:
                user.jurisdiction.clear()
                if jurisdiction := data['jurisdiction']:
                    jurs = Jurisdiction.objects.filter(pk__in=jurisdiction)
                    for i in jurs:
                        user.jurisdiction.add(i)
            if u := request.data.get('userinfo'):
                userinfo = user.userinfo
                if name := u.get('name'):
                    userinfo.name = name
                userinfo.save()
            user.save()
            return Response({'code': 200, 'msg': 'Update successful!', 'data': None})
        return Response({'code': 400, 'msg': 'Data does not exist!', 'data': None})

    def delete(self, request, id=None):
        if user := User.objects.filter(pk=id).first():
            user.delete()
            return Response({'code': 200, 'msg': 'Delete successful!'})
        return Response({'code': 400, 'msg': 'Data does not exist!', 'data': None})
