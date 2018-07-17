from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, decorators
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from album.models import Album, AlbumMemberShip, AlbumPhotoShip
from album.serializers import AlbumSerializer, AlbumMemberShipSerializer, AlbumPhotoShipSerializer
from album.filters import AlbumFilter
from rest_framework import status
from rest_framework.response import Response


class AlbumViewSet(viewsets.ModelViewSet):
    """
    Album view
    相册 视图
    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = AlbumFilter
    search_fields = ('name', 'description')
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        # 创建相册
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {'data': serializer.data,
                         'status': 'SUCCESS',
                         'message': '相册创建成功'}
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        # 正常情况下返回status为normal的相册
        queryset = self.filter_queryset(self.get_queryset().filter(Q(status="normal")))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @decorators.action(detail=False, methods=('GET',))
    def recycler(self, request, pk=None):
        # 状态为回收站
        queryset = Album.objects.filter(Q(folder__user=self.request.user), Q(status="recycler"))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Album.objects.filter(Q(user=self.request.user), Q(status="normal"))


class AlbumMemberInvitationViewSet(viewsets.ModelViewSet):
    """
        AlbumMenber view
        相册成员关系 视图
    """
    queryset = AlbumMemberShip.objects.all()
    serializer_class = AlbumMemberShipSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_class = AlbumFilter
    search_fields = ('album', 'member')
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        # 邀请新成员
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {'data': serializer.data,
                         'status': 'SUCCESS',
                         'message': '邀请成功'}
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class AlbumPhotoAdderViewSet(viewsets.ModelViewSet):
    """
    AlbumPhoto view
    相册照片关系 视图
    """
    queryset = AlbumPhotoShip.objects.all()
    serializer_class = AlbumPhotoShipSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_class = AlbumFilter
    search_fields = ('album', 'photo')
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        # 添加新照片
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {'data': serializer.data,
                         'status': 'SUCCESS',
                         'message': '添加成功'}
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


#
# class AlbumUserRelationViewSet(viewsets.ModelViewSet):
#     queryset = AlbumUserRelation.objects.all()
#     serializer_class = AlbumUserRelationSerializer
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
#     filter_class = AlbumFilter
#     search_fields = ('name', 'description')
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#
#
# class AlbumPhotoRelationViewSet(viewsets.ModelViewSet):
#     queryset = AlbumPhotoRelation.objects.all()
#     serializer_class = AlbumPhotoRelationSerializer
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
#     filter_class = AlbumFilter
#     search_fields = ('name', 'description')
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)


