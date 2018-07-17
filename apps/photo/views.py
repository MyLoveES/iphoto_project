# -*- coding: utf-8 -*-
import json
import urllib
from urllib.parse import unquote
import traceback
from pykafka import KafkaClient
from rest_framework import decorators
from django.shortcuts import render
from django.db.models import Q
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle
from urllib3 import HTTPResponse

from face.models import Face, FaceFile
from photo.models import Photo, Category, Entity, PhotoEntity
from folder.models import Folder
# from django.views.generic import ListView
from photo.serializers import PhotoSerializer, CategorySerializer, EntitySerializer, PhotoEntitySerializer
from folder.serializers import FolderSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from photo.filters import PhotoFilter
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from photo.tasks import kafka_produce, mul, face_detect, face_recognition
from util.checks import check_owner
from util.permissions import IsOwnerOrReadOnly
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from redis import Redis


class PhotoViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    """
    Photo view
    照片 视图
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = PhotoFilter
    search_fields = ('name', 'description')
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        # request.data['user'] = request.user.id
        # 判断文件夹是否存在
        try:
            try:
                if "folder" not in request.data:
                    response_data = {'data': '',
                                     'status': 'Failure',
                                     'message': '参数错误, 需要folder参数'}
                    return Response(response_data, status.HTTP_400_BAD_REQUEST)
                folder = Folder.objects.filter(Q(name__exact=request.data['folder']),
                                           Q(user__exact=request.user))
            except Exception as e:
                print('str(Exception):\t', str(Exception))
                print('str(e):\t\t', str(e))
                print('repr(e):\t', repr(e))
                print('traceback.print_exc():', traceback.print_exc())
                print('traceback.format_exc():\n%s' % traceback.format_exc())
                response_data = {'data': '',
                                 'status': 'Failure',
                                 'message': '参数错误, 需要folder参数'}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            # 如果文件夹不存在, 创建文件夹, 否则返回存在的文件夹ID
            if not folder.exists():
                print('Creating folder')
                folder = Folder(name=request.data['folder'], user=request.user)
                folder.save()
                request.data.__setitem__('folder', folder.id)
            else:
                request.data.__setitem__('folder', folder.first().id)

            if Folder.objects.filter(Q(user=request.user), Q(id=request.data['folder'])).first() is None:
                # 判断该文件夹是否属于该用户，其实没用。不属于会创建。
                response_data = {
                    'folder': '这文件夹不是你的！',
                }
                return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

            # 如果有文件上传
            if request.FILES:
                print('FILES TRUE:', request.data)
                post_data = request.data
                response_data = []
                if "file" not in request.FILES:
                    response_data = {'data': '',
                                     'status': 'Failure',
                                     'message': '参数错误, 需要file参数'}
                    return Response(response_data, status.HTTP_400_BAD_REQUEST)
                for file in request.FILES.getlist('file'):
                    try:
                        # 若未指定文件名，默认文件名
                        post_data['name'] = file.name
                        # 获得文件列表文件
                        post_data['file'] = file
                    except Exception as e:
                        print('str(Exception):\t', str(Exception))
                        print('str(e):\t\t', str(e))
                        print('repr(e):\t', repr(e))
                        print('traceback.print_exc():', traceback.print_exc())
                        print('traceback.format_exc():\n%s' % traceback.format_exc())
                        response_data = {'data': '',
                                         'status': 'Failure',
                                         'message': '参数错误,需要name, file参数'}
                        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                    # 写入数据库，服务器保存
                    serializer = self.get_serializer(data=post_data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)
                    response_data.append(
                        {
                            'data': serializer.data,
                            'status': 'SUCCESS',
                            'message': '上传成功',
                        }
                    )
                    kafka_message = {
                        "token": "detection",
                        "user": request.user.id,
                        "photo": serializer.data.get('id'),
                        "photo_filepath": urllib.parse.unquote(serializer.data.get('file'))
                    }
                    # mul.delay(5, 7)
                    # celery 进行识别工作
                    kafka_produce.delay(kafka_message)
                return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                # 无文件上传
                response_data = {
                    'data': None,
                    "message": "无文件上传",
                    "status": "FAILURE"
                }
                Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            print('traceback.print_exc():', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            response_data = {'data': '',
                             'status': 'Failure',
                             'message': '发生错误'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        # 正常情况下返回status为normal的照片
        queryset = self.filter_queryset(self.get_queryset().filter(Q(status="normal")))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # 如果查询分类，则进行返回
        category_list = ['person', 'transport', 'animal', 'office', 'sport', 'gourmet', 'furniture']
        url = self.get_url()
        # 如果是人脸，返回
        if url == "face":
            response_data = {}
            face_queryset = Face.objects.filter(user=request.user)
            for face in face_queryset:
                facefile_queryset = FaceFile.objects.filter(Q(face=face), Q(photo__in=self.get_queryset().filter(status='normal')))
                if facefile_queryset.exists():
                    response_data[face.face] = {}
                    for facefile in facefile_queryset:
                        response_data[face.face][facefile.photo.id] = facefile.photo.path
                else:
                    face.delete()
                    continue
            return Response(response_data)
        elif url not in category_list:
            # 否则返回正常Retrieve请求的数据
            return super(PhotoViewSet, self).retrieve(request, *args, **kwargs)
        else:
            response_data = {}
            photoentity_set = PhotoEntity.objects.filter(Q(entity__category__category=url),
                                                         Q(photo__in=self.get_queryset()))
            entity_set = photoentity_set.values_list('entity').distinct()
            for entity in entity_set:
                entity_name = Entity.objects.filter(id=list(entity)[0]).first().entity
                response_data[entity_name] = {}
                for photo in photoentity_set.filter(Q(entity=entity)).values_list('photo'):
                    response_data[entity_name][list(photo)[0]] = Photo.objects.filter(id=list(photo)[0]).first().path
            return Response(response_data)

    # 回收站数据
    @decorators.action(detail=False, methods=('GET',))
    def recycler(self, request, pk=None):
        queryset = Photo.objects.filter(Q(folder__user=self.request.user), Q(status="recycler"))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # 获取Retrieve的url
    def get_url(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        url = self.kwargs[lookup_url_kwarg]
        return url

    # 管理员获取所有，用户获取私有
    def get_queryset(self):
        if self.request.user.is_superuser is True:
            return self.queryset.all()
        else:
            return self.queryset.filter(Q(folder__user=self.request.user))

    # 持久化
    def perform_create(self, serializer):
        return serializer.save()

    # ordering_fields = ('sold_num', 'shop_price')
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.click_num += 1
    #     instance.save()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Category view
    类别 视图
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('category', )


class EntityViewSet(viewsets.ModelViewSet):
    """
    Entity view
    实体 视图
    """
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('entity', 'category')


class PhotoEntityViewSet(viewsets.ModelViewSet):
    """
    PhotoEntity view
    照片实体关系 视图
    """
    queryset = PhotoEntity.objects.all()
    serializer_class = PhotoEntitySerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        # 照片实体建立联系
        # 判断token是否存在
        if "token" not in request.data:
            return super(PhotoEntityViewSet, self).create(request, *args, **kwargs)
        else:
            photo = request.data["photo"]
            category_data = request.data["category_data"]
            response_data = []
            for category in category_data.keys():
                entity_data = category_data[category]
                if len(entity_data) == 0:
                    continue
                for entity in entity_data:
                    entity_id = Entity.objects.filter(Q(category__category=category), Q(entity=entity)).first().id
                    db_data = {
                        "photo": photo,
                        "entity": entity_id
                    }
                    serializer = self.get_serializer(data=db_data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)
                    response_data.append({
                            'data': serializer.data,
                            'status': 'SUCCESS',
                            'message': '识别成功',
                        })
            return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        if self.request.user.is_superuser is True:
            return self.queryset
        else:
            return self.queryset.filter(Q(photo__folder__user=self.request.user))