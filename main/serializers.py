from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'icon', 'name') #'__all__'

class FieldSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Field
        fields = [field.name for field in model._meta.fields]
        fields.append('id')
        fields.append('tags')

    def get_tags(self, obj):
        selected_tags = Tag.objects.filter(field_id=obj.id).distinct()
        return TagSerializer(selected_tags, many=True).data


class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DefUser
        fields = '__all__' #['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']