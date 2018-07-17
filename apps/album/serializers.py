from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from album.models import Album, AlbumPhotoShip, AlbumMemberShip
from django.contrib import auth


class AlbumSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    photos = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='photo-detail')
    members = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='userprofile-detail')
    # albummembership_album = serializers.HyperlinkedRelatedField(many=True, read_only=True,
    #                                                             view_name='albummembership-detail')
    # albumphotoship_album = serializers.HyperlinkedRelatedField(many=True, read_only=True,
    #                                                            view_name='albumphotoship-detail')

    class Meta:
        model = Album
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Album.objects.all(),
                fields=('user', 'name'),
                message='同一用户不允许创建同名相册'
            )
        ]


class AlbumMemberShipSerializer(serializers.ModelSerializer):
    inviter = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, attrs):
        user = attrs['inviter']
        album = attrs['album']
        member = attrs['member']
        print("validate", user, album)
        if album not in user.album_user.all():
            raise serializers.ValidationError("邀请者不属于该相册")
        elif user == member:
            raise serializers.ValidationError("不能邀请自己")
        elif member == album.user:
            raise serializers.ValidationError("相册创建者已是成员")
        return attrs

    class Meta:
        model = AlbumMemberShip
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=AlbumMemberShip.objects.all(),
                fields=('album', 'member'),
                message='该相册已共享给该用户'
            )
        ]


class AlbumPhotoShipSerializer(serializers.ModelSerializer):
    adder = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, attrs):
        user = attrs['adder']
        album = attrs['album']
        photo = attrs['photo']
        print("validate", user, album)
        if album not in user.album_user.all():
            raise serializers.ValidationError("添加者不属于该相册")
        elif photo.folder not in user.folder_user.all():
            raise serializers.ValidationError("该照片不属于该添加者")
        return attrs

    class Meta:
        model = AlbumPhotoShip
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=AlbumPhotoShip.objects.all(),
                fields=('album', 'photo'),
                message='该相册已有此照片'
            )
        ]


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