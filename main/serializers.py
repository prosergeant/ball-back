from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'icon', 'name') #'__all__'

class FieldSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.SerializerMethodField()
    field_types = serializers.SerializerMethodField()
    owner_id = serializers.SerializerMethodField()

    class Meta:
        model = Field
        fields = [field.name for field in model._meta.fields]
        fields.append('id')
        fields.append('tags')
        fields.append('field_types')
#         fields.pop('owner')
        fields.append('owner_id')

    def get_tags(self, obj):
        selected_tags = Tag.objects.filter(field_id=obj.id).distinct()
        return TagSerializer(selected_tags, many=True).data

    def get_field_types(self, obj):
        selected_field_types = FieldType.objects.filter(field_id=obj.id).distinct()
        return FieldTypeSerializer(selected_field_types, many=True).data

    def get_owner_id(self, obj):
        owner = DefUser.objects.filter(id=obj.owner.id).first()
        if owner is None:
            return ""
        return owner.id

class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = '__all__'
        depth=1


class RequestSerializerPost(serializers.ModelSerializer):
    is_ended = serializers.ReadOnlyField()

    class Meta:
        model = Request
        fields = '__all__'

    def validate(self, data):
        queryset = Request.objects.filter(
            field_type=data.get('field_type', 'null'),
            date=data.get('date', 'null'),
            time=data.get('time', 'null'),
            paid=True
        )
        if queryset.exists():
            raise serializers.ValidationError("поля date, time должны быть уникальными")
        return data


class RequestSerializerPatch(serializers.ModelSerializer):
    is_ended = serializers.ReadOnlyField()

    class Meta:
        model = Request
        fields = '__all__'


class RequestSerializerGet(serializers.ModelSerializer):
    field_type = FieldTypeSerializer()
    is_ended   = serializers.ReadOnlyField()

    class Meta:
        model = Request
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DefUser
        fields = [field.name for field in model._meta.fields]
        fields.append('id')

    def create(self, validated_data):
        user = DefUser.objects.create(
            phone = validated_data['phone'],
            name = validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
