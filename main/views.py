from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer


class FieldTypeViewSet(viewsets.ModelViewSet):
#     queryset = FieldType.objects.all()
    serializer_class = FieldTypeSerializer

    def get_queryset(self):
        queryset = FieldType.objects.all()
        field = self.request.query_params.get('field')
        if field is not None:
            queryset = queryset.filter(field_id=field)
        return queryset


class RequestViewSet(viewsets.ModelViewSet):
#     queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def get_queryset(self):
        queryset = Request.objects.all()
        field_type = self.request.query_params.get('fieldtype')
        date = self.request.query_params.get('date')
        user_id = self.request.query_params.get('user')
        if field_type is not None:
            queryset = queryset.filter(field_type_id=field_type)
        if date is not None:
            queryset = queryset.filter(date=date)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset


class SendOTPApiView(APIView):
    def post(self, request):
        otp = request.data.get('otp')
        phone_number = request.data.get('phone')

        response = requests.post('https://smsc.kz/rest/send/', json = {
            "login": "sberendeyev",
            "psw": "Killer1996",
            "phones": phone_number,
            "mes": f"bronkz: {otp}"
        })

        return Response(status=200)


class UserViewSet(viewsets.ModelViewSet):
    queryset = DefUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    http_method_names = ['post']
#     permission_classes = [permissions.IsAuthenticated]

class GetUserInfo(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = DefUser.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]