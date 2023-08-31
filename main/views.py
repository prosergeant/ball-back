from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all().order_by('id')
    serializer_class = FieldSerializer

    def get_queryset(self):
        queryset = Field.objects.all()
        field = self.request.query_params.get('field')
        if field is not None:
            queryset = queryset.filter(id=field)
        return queryset


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
#     serializer_class = RequestSerializer
    def get_serializer_class(self):
         if self.request.method in ['GET']:
             return RequestSerializerGet
         elif self.request.method in ['PATCH']:
             return RequestSerializerPatch
         return RequestSerializerPost

    def get_queryset(self):
        queryset = Request.objects.all().order_by('-id')
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
    queryset = DefUser.objects.all() #.order_by('-date_joined')
    serializer_class = UserSerializer
    http_method_names = ['post']
#     permission_classes = [permissions.IsAuthenticated]

class GetUserInfo(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = DefUser.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class ChangeUserPassword(APIView):
#     permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        phone = request.data.get('phone')
        if phone is None:
            return Response(status=400)
        user = DefUser.objects.filter(phone=phone).first() #(id=request.user.id)
        if user is None:
            return Response(status=400)
        user.set_password(request.data.get('password'))
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class FindUserByPhone(APIView):
    def post(self, request, format=None):
        user = DefUser.objects.filter(phone=request.data.get('phone'))

        if len(user) > 0:
            return Response(status=400)
        return Response(status=200)


class SetNewImage(APIView):
    def post(self, request, *args, **kwargs):
        image = request.FILES.get('image')
        user = DefUser.objects.filter(id=request.user.id).first()
        if user is None:
            return Response({"error": "user not found"}, status=400)
        user.photo = image
        user.save()
        return Response(status=200)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
