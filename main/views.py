from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from .models import *
from rest_framework.response import Response

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
        if field_type is not None:
            queryset = queryset.filter(field_type_id=field_type)
        if date is not None:
            queryset = queryset.filter(date=date)
        return queryset

    def create(self, request, *args, **kwargs):
        req_keys = ['date', 'time', 'field_type', 'user']
        data = request.data

        if len(data) != 4:
            return Response({"error": "too many arguments"}, status=422)

        for i in data:
            if (i in req_keys) == False:
                return Response({"error": "not req_keys"}, status=422)

        date = data.get('date')
        time = data.get('time')
        field_type_id = data.get('field_type')
        user_id = data.get('user')

        if date is None:
            return Response({"error": "date field is Node"}, status=422)
        if time is None:
            return Response({"error": "time field is Node"}, status=422)

        same_date = Request.objects.filter(date=date, time=time)
        if len(same_date) > 0:
            return Response({"error": "this time already exists"}, status=422)

        new_request = Request(
            date=date,
            time=time,
            user_id=user_id,
            field_type_id=field_type_id
        )
        new_request.save()

        return Response(status=200)


class UserViewSet(viewsets.ModelViewSet):
    queryset = DefUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]