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
        user_id = self.request.query_params.get('user_id')
        user = DefUser.objects.filter(id=user_id).first()
        if field is not None:
            queryset = queryset.filter(id=field)
        if user is not None:
            queryset = queryset.filter(owner_id=user.id)
        return queryset


class FieldPhotoViewSet(viewsets.ModelViewSet):
    serializer_class = FieldPhotoSerializer

    def get_queryset(self):
        queryset = FieldPhoto.objects.all()
        field = self.request.query_params.get('field')
        if field is not None:
            queryset = queryset.filter(field_id=field)
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


class DeleteUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = DefUser.objects.filter(id=request.user.id).first()
        if user is None:
            return Response(status=404)
        user.delete()
        return Response(status=200)


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


class ChangeUserFcmToken(APIView):
    def post(self, request, format=None):
        phone = request.data.get('phone')
        token = request.data.get('fcmToken')
        if phone is None or token is None:
            return Response(status=400)
        user = DefUser.objects.filter(phone=phone).first() #(id=request.user.id)
        if user is None:
            return Response(status=400)
        user.fcmToken = token
        user.save()
        return Response(status=200)


class SendNotifyToUser(APIView):
    def post(self, request, format=None):
        phone = request.data.get('phone')
        title = request.data.get('title')
        body = request.data.get('body')
        sound = request.data.get('sound')
        badge = request.data.get('badge')

        if phone is None or title is None or body is None:
            return Response(status=400)

        if sound is None:
            sound = 'default'
        if badge is None:
            badge = 1

        user = DefUser.objects.filter(phone=phone).first() #(id=request.user.id)
        if user is None:
            return Response(status=400)

        url = 'https://fcm.googleapis.com/fcm/send'
        headers = {'Authorization': 'key=AAAAUdFgUgs:APA91bH1eR_Gk-5SNFMNnHag-ODuPYBUEXvnfDrJgqUhjmZAnc6W5dNKQr_nT3KBe11qEj60nfGwMNjPp-zlG1ExKCsMeQR-HaDFumRNkBwIedrBhHBhVz99aN_HRvnxfCbEcntrkui4'}
        res = requests.post(url, headers=headers, json = {
            "to": user.fcmToken,
            "notification": {
                "title": title,
                "body": body,
                "sound": sound,
                "badge": badge
            }
         })

        print(res.status_code)
        print(res.text)

        return Response(status=200)


class FindUserByPhone(APIView):
    def post(self, request, format=None):
        user = DefUser.objects.filter(phone=request.data.get('phone'))

        if len(user) > 0:
            return Response(status=400)
        return Response(status=200)


class FindUserById(APIView):
    def get(self, request, format=None):
        user = DefUser.objects.filter(id=request.query_params.get('id')).first()

        if user is None:
            return Response(status=400)

        serializer = UserSerializer(user)
        return Response(serializer.data)


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
