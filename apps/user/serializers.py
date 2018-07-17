import datetime
from rest_framework import serializers
from iphoto_project.settings import REGEX_MOBILE, VERIFY_CODE
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
import re

from util.redis_connect import rds_for_verify

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)

    def validate_phone(self, phone):
        """
        验证手机号码
        :param data:
        :return:
        """

        # 手机是否注册
        if User.objects.filter(username=phone).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, phone):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        if rds_for_verify.get(phone):
            raise serializers.ValidationError("距离上一次发送未超过1min")

        return phone

    def save(self, **kwargs):
        validated_data = dict(list(self.validated_data.items()) + list(kwargs.items()))
        result = rds_for_verify.set(name=validated_data['phone'],
                                    value=kwargs.pop('verify_code'),
                                    ex=60)
                                    # ex=60 * 5)
        return result


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    folder_user = serializers.HyperlinkedRelatedField(many=True,
                                                      read_only=True,
                                                      view_name='folder-detail')
    album_user = serializers.HyperlinkedRelatedField(many=True,
                                                     read_only=True,
                                                     view_name='album-detail')

    class Meta:
        model = User
        fields = ('id', 'last_login', 'username', 'first_name', 'email', 'password', 'folder_user', 'album_user')
        extra_kwargs = {
            "username": {'read_only': True},
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    # phone = serializers.CharField(label="手机", help_text="手机", required=True, allow_blank=False, allow_null=False,
    #                               error_messages={
    #                                   "null": "请输入手机号",
    #                                   "blank": "请输入手机号",
    #                                   "required": "请输入手机号",
    #                               },
    #                               validators=[UniqueValidator(queryset=User.objects.all(),
    #                                                           message={'status': "手机已被注册",
    #                                                                    'code': 10})])
    code = serializers.CharField(label="验证码", help_text="验证码", required=True, allow_blank=False, allow_null=False,
                                 write_only=True,
                                 error_messages={
                                     "null": "请输入验证码",
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                 }, )
    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False, allow_null=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message="用户名已经存在")])

    def validate_code(self, code):
        if not re.match(VERIFY_CODE, code):
            raise serializers.ValidationError("验证码格式错误")

    def validate(self, attrs):
        rds_for_verify.delete(attrs['username'])
        del attrs['code']
        return attrs

    def validate_username(self, username):
        """
        验证手机号码
        :param data:
        :return:
        """
        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, username):
            raise serializers.ValidationError("手机号码格式非法")
        if not rds_for_verify.get(username):
            raise serializers.ValidationError("验证码过期/尚未发送验证码")
        if rds_for_verify.get(username).decode() != self.initial_data['code']:
            raise serializers.ValidationError("验证码错误")

        return username

    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data=validated_data)
        if user.first_name is (None or ""):
            user.first_name = user.username
        user.is_staff = True
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'code')


# class UserLoginSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = ('phone', 'password')

# class UserPhotoSerializer(serializers.HyperlinkedModelSerializer):
#
#     # photo = PhotoSerializer(many=True)
#
#     class Meta:
#         model = User
#         fields = '__all__'
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
#
#     class Meta:
#         model = User
#         fields = ('url', 'id', 'username', 'snippets')

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
