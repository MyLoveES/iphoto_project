# -*- coding: utf-8 -*-
import random

from django.db.models import Q
from django.shortcuts import render
import traceback
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework import decorators
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle
# from photo.models import Photo
from django.contrib.auth.backends import ModelBackend
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from photo.serializers import PhotoSerializer
from folder.serializers import FolderSerializer
# from django.views.generic import ListView
from user.serializers import UserListSerializer, UserRegisterSerializer, UserSerializer, SmsSerializer
from rest_framework.reverse import reverse
import jwt
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from util.dysms_python.demo_sms_send import send_for_sys
from util.encryption import generate_code
from util.get_ip import get_client_ip
from util.permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # user = User.objects.get(Q(username=username) | Q(phone=username) | Q(email=username))
            user = User.objects.get(Q(username=username))
            if user.check_password(password):
                return user
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            print('traceback.print_exc():', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            return None


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        # 注册
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.perform_create(serializer)

            re_dict = serializer.data
            payload = jwt_payload_handler(user)
            re_dict["token"] = jwt_encode_handler(payload)

            headers = self.get_success_headers(serializer.data)
            response_data = {'token': re_dict,
                             'status': 'SUCCESS',
                             'message': '注册成功'}
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            print('traceback.print_exc():', traceback.print_exc())
            print( 'traceback.format_exc():\n%s' % traceback.format_exc())
            response_data = {'token': '',
                             'status': 'Failure',
                             'message': '发生错误'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return []
        else:
            return [IsAuthenticated(), ]

    @decorators.action(detail=True, methods=('GET', 'LIST', 'RETRIEVE',))
    def photos(self, request, pk=None):
        photo_queryset = User.objects.get(pk=pk).user_related_photos.all()
        if photo_queryset.exists():
            serializer = PhotoSerializer(photo_queryset, many=True, context={'request': request})
            return Response(serializer.data)

    @decorators.action(detail=True, methods=('GET', 'LIST', 'RETRIEVE',))
    def folders(self, request, pk=None):
        folder_queryset = User.objects.get(pk=pk).user_related_folders.all()
        if folder_queryset.exists():
            serializer = FolderSerializer(folder_queryset, many=True, context={'request': request})
            return Response(serializer.data)

    def get_queryset(self):
        with open('client_ip.txt', 'a+') as f:
            f.write(get_client_ip(self.request)+"\n")
        f.close()
        return User.objects.filter(id=self.request.user.id)

    def get_object(self, queryset=None):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            phone = serializer.validated_data["phone"]
            code = generate_code()

            sms_status = send_for_sys(phone_numbers=phone, verify_code=code)
            print(sms_status["Code"])

            if sms_status["Code"] != 'OK':
                return Response({
                    "code": "null",
                    "status": "FAILURE",
                    "message": sms_status["Message"]
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save(verify_code=code)
                return Response({
                    "code": code,
                    "status": "SUCCESS",
                    "message": sms_status["Message"]
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            print('traceback.print_exc():', traceback.print_exc())
            print( 'traceback.format_exc():\n%s' % traceback.format_exc())
            response_data = {'token': '',
                             'status': 'Failure',
                             'message': '发生错误'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
# class UsersRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserRegisterSerializer

    # def create(self, request, *args, **kwargs):
    #     # if 'name' not in request.POST:
    #     #     # request.data.append('name', request.data['phone'])
    #         mutable = request.POST._mutable
    #         request.POST._mutable = True
    #         request.data['name'] = request.data['phone']
    #         request.POST._mutable = mutable
    #     mutable = request.POST._mutable
    #     request.POST._mutable = True
    #     request.data.setdefault('username', request.POST['phone'])
    #     print(request.data)
    #     request.data['username'] = request.POST['phone']
    #     print(request.data)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     response_body = {"status": True, "User": serializer.data['phone']}
    #     return Response(response_body, status=status.HTTP_201_CREATED, headers=headers)


# class UsersLoginViewSet(mixins.CreateModelMixin, viewsets.ViewSet):
#     # queryset = User.objects.all()
#     serializer_class = UserLoginSerializer
#
#     def create(self, request, *args, **kwargs):
#         print(request.POST['username'], request.POST['password'])
#         if User.objects.filter(Q(username=request.POST['username']), Q(password=request.POST['password'])) or\
#                 User.objects.filter(Q(phone=request.POST['username']), Q(password=request.POST['password'])):
#             return Response({"status": True}, status=status.HTTP_200_OK)
#         else:
#             return Response({"status": False}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
#
#
# class UsersJwtLoginViewSet(mixins.CreateModelMixin, viewsets.ViewSet):
#     # queryset = User.objects.all()
#     serializer_class = UserLoginSerializer
#
#     def create(self, request, *args, **kwargs):
#         print(request.POST['phone'], request.POST['password'])
#         if User.objects.filter(Q(phone=request.POST['phone']), Q(password=request.POST['password'])):
#             return Response({"status": True}, status=status.HTTP_200_OK)
#         else:
#             return Response({"status": False}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
#





