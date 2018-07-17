from rest_framework import serializers
from photo.models import Photo, Category, Entity, PhotoEntity
from folder.models import Folder
from django.contrib import auth

from util.checks import check_owner


class PhotoEntityField(serializers.RelatedField):
    def to_representation(self, value):
        return value.entity.entity


class PhotoSerializer(serializers.ModelSerializer):
    photoentity_photo = PhotoEntityField(many=True, read_only=True)

    class Meta:
        model = Photo
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class EntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entity
        fields = '__all__'


class PhotoEntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = PhotoEntity
        fields = '__all__'

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
#
#     class Meta:
#         model = User
#         fields = ('url', 'id', 'username', 'snippets')
#
# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance