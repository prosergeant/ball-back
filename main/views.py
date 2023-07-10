from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from .models import *

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


class UserViewSet(viewsets.ModelViewSet):
    queryset = DefUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]