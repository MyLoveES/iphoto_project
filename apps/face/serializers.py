from rest_framework import serializers

from face.models import Face, FaceFile
from folder.models import Folder
from django.conf import settings

#
# class FaceSerializer(serializers.Serializer):
#     image = serializers.FileField(required=True)
#     machine_code = serializers.CharField(required=True, allow_blank=False, allow_null=False, max_length=100, help_text="机器识别码")
#     # user_info = serializers.CharField(required=True, allow_blank=False, allow_null=False, max_length=100, help_text="名字")


class FaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Face
        fields = '__all__'


class FaceFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = FaceFile
        fields = '__all__'
# class FolderCreateSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Folder
#         fields = ('name', 'user')
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