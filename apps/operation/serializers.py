from django.conf import settings
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueTogetherValidator

from album.models import Album
from django.contrib import auth
from operation.models import ShareObject
from datetime import datetime

# class ShareOperationSerializer(serializers.Serializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#     password = serializers.CharField()
#     photos = serializers.ListField(child=serializers.IntegerField())
#     folders = serializers.ListField(child=serializers.IntegerField())
#     share_time = serializers.DateTimeField(default=datetime.now())
#     ttl = serializers.IntegerField(write_only=True)
#
#     def create(self, validated_data):
#         print("Creating")
#         print("validated_data", type(validated_data), validated_data)
#         return ShareObject(**validated_data)
#
#     def update(self, instance, validated_data):
#         print("Updating:", instance)
#         instance.password = validated_data.get('password', instance.password)
#         instance.folders = validated_data.get('folders', instance.folders)
#         instance.photos = validated_data.get('photos', instance.photos)
#         return instance
#
#     def save(self, **kwargs):
#         url = kwargs.pop('url', None)
#         partial = kwargs.pop('partial', False)
#         ttl = kwargs.pop('ttl', -1)
#         instance = kwargs.pop('instance', None)
#         validated_data = dict(
#             list(self.validated_data.items())
#         )
#         del validated_data['ttl']
#         if not partial:
#             self.instance = self.create(validated_data)
#         else:
#             self.instance = self.update(instance=instance, validated_data=validated_data)
#
#         return self.instance.save(url=url, ttl=ttl)


class ShareOperationSerializer(serializers.Serializer):
    photos = serializers.ListField(child=serializers.IntegerField())
    folders = serializers.ListField(child=serializers.IntegerField())
    ttl = serializers.IntegerField(write_only=True, default=-1)

    def validate(self, attrs):
        photos = self.initial_data['photos']
        folders = self.initial_data['folders']
        if ((photos is None) or len(photos) == 0) and ((folders is None) or len(folders) == 0):
            raise serializers.ValidationError("无分享内容")
        return attrs
    # def create(self, validated_data):
    #     print("Creating")
    #     print("validated_data", type(validated_data), validated_data)
    #     return ShareObject(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     print("Updating:", instance)
    #     instance.password = validated_data.get('password', instance.password)
    #     instance.folders = validated_data.get('folders', instance.folders)
    #     instance.photos = validated_data.get('photos', instance.photos)
    #     return instance
    #
    # def save(self, **kwargs):
    #     url = kwargs.pop('url', None)
    #     partial = kwargs.pop('partial', False)
    #     ttl = kwargs.pop('ttl', -1)
    #     instance = kwargs.pop('instance', None)
    #     validated_data = dict(
    #         list(self.validated_data.items())
    #     )
    #     del validated_data['ttl']
    #     if not partial:
    #         self.instance = self.create(validated_data)
    #     else:
    #         self.instance = self.update(instance=instance, validated_data=validated_data)
    #
    #     return self.instance.save(url=url, ttl=ttl)

# class AlbumUserRelationSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = AlbumUserRelation
#         fields = '__all__'
#
#
# class AlbumPhotoRelationSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = AlbumPhotoRelation
#         fields = '__all__'
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


class EditionSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    editionCode = serializers.CharField(allow_blank=False, max_length=10,
                                        label="版本号", help_text="版本号", required=True, allow_null=False,
                                        error_messages={
                                             "null": "请输入版本号",
                                             "blank": "请输入版本号",
                                             "required": "请输入版本号",
                                         }, )
    changeLog = serializers.CharField(allow_blank=True, max_length=1000,
                                      label="更新日志", help_text="更新日志", required=False, allow_null=True,
                                      )
    url = serializers.CharField(read_only=True, max_length=100, min_length=100)
    apkFile = serializers.FileField()
