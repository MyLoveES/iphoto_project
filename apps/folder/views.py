# -*- coding: utf-8 -*-
import traceback

from django.shortcuts import render
from django.db.models import Q
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework import mixins, decorators
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle
from folder.models import Folder
# from django.views.generic import ListView
from folder.serializers import FolderSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from folder.filters import FolderFilter
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from util.permissions import IsOwnerOrReadOnly


class FolderViewSet(viewsets.ModelViewSet):
    """
    Folder view
    文件夹 视图
    """
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = FolderFilter
    search_fields = ('name',)
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        try:
            # 查询文件夹是否存在
            print(request.data)
            if "name" not in request.data:
                response_data = {'data': '',
                                 'status': 'Failure',
                                 'message': '参数错误, 需要name参数'}
                return Response(response_data, status.HTTP_400_BAD_REQUEST)
            folder = Folder.objects.filter(Q(name__exact=request.data['name']),
                                           Q(user=request.user))
            # 如果存在返回文件夹ID
            if folder.exists():
                return Response({'status': 'exists',
                                 'folder_id': folder.first().id},
                                status=status.HTTP_302_FOUND)
            # 不存在，持久化
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            response_data = {
                'data': serializer.data,
                'status': 'SUCCESS',
                'message': '文件夹创建成功'
            }
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            print('traceback.print_exc():', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            response_data = {'token': '',
                             'status': 'Failure',
                             'message': '发生错误'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        # 一般情况下返回status为normal的文件夹
        queryset = self.filter_queryset(self.get_queryset().filter(Q(status="normal")))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @decorators.action(detail=False, methods=('GET',))
    def recycler(self, request, pk=None):
        # 返回status为recycler的文件夹
        queryset = Folder.objects.filter(Q(user=self.request.user), Q(status="recycler"))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        # 管理员返回所有，用户返回私有
        if self.request.user.is_superuser is True:
            return self.queryset
        else:
            return self.queryset.filter(Q(user=self.request.user))

    def perform_create(self, serializer):
        # 持久化
        return serializer.save()

# class FolderOperateViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
#                            mixins.UpdateModelMixin, viewsets.GenericViewSet):
#     queryset = Folder.objects.all()
#     serializer_class = FolderCreateSerializer




