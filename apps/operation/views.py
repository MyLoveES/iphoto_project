import json

from django.http import JsonResponse

from rest_framework import status, viewsets, generics, mixins, decorators
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import views
from datetime import datetime
from time import time

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from folder.models import Folder
from operation.models import ShareObject, ShareAuthObject, EditionObject
from operation.serializers import ShareOperationSerializer, EditionSerializer
from photo.models import Photo
from util.encryption import make_share_url, make_share_password


# class ShareOperationViewSet(viewsets.GenericViewSet,
#                             mixins.CreateModelMixin,
#                             mixins.UpdateModelMixin,
#                             mixins.RetrieveModelMixin,
#                             mixins.DestroyModelMixin,):
#
#     serializer_class = ShareOperationSerializer
#
#     def create(self, request, *args, **kwargs):
#         url = make_share_url()
#         ttl = request.data['ttl']
#         request.data['password'] = make_share_password()
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(url=url, ttl=ttl)
#         share_data = {
#             'url': url,
#             'password': request.data['password']
#         }
#         return Response(share_data)
#
#     def retrieve(self, request, *args, **kwargs):
#         obj = self.get_instance()
#         if not obj:
#             return Response(data="链接已失效")
#         serializer = self.get_serializer(obj)
#         return Response(serializer.data)
#
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_instance()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         share_data = serializer.save(url=self.get_url(), instance=instance, partial=partial)
#         return Response(share_data)
#
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_instance()
#         delete = instance.delete(self.get_url())
#         return Response(data=delete, status=status.HTTP_204_NO_CONTENT)
#
#     def get_object(self, queryset=None):
#         # obj = rds.get(self.get_url()).decode().replace("'", "\"")
#         obj = rds_for_share.get(self.get_url())
#         if not obj:
#             return None
#         return eval(obj)
#
#     def get_instance(self):
#         instance = self.get_object()
#         if not instance:
#             return None
#         # return ShareObject(instance['user'], instance['password'], instance['folders'], instance['photos'])
#         return ShareObject(**instance)
#
#     def get_url(self):
#         lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
#         url = self.kwargs[lookup_url_kwarg]
#         return url

class ShareOperationViewSet(viewsets.GenericViewSet,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin, ):

    serializer_class = ShareOperationSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    @decorators.action(detail=True, methods=('POST',))
    def auth(self, request, pk=None):
        auth_data = ShareAuthObject.get(url=pk)
        if not auth_data:
            response_data = {
                "status": "FAILURE",
                "message": "链接已失效",
            }
        else:
            if request.data['password'] == auth_data.get("password"):
                response_data = {
                    "mongoid": auth_data.get("mongoid"),
                    "status": "ok"
                }
            else:
                response_data={
                    "message": "密码错误",
                    "status": "FAILURE"
                }
        return Response(data=response_data)

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = make_share_url()
        share_time = datetime.utcnow()
        folders = request.data['folders']
        photos = []

        password = make_share_password()
        ttl = request.data['ttl']

        # photos = request.data['photos']
        # folders = []
        for photo in request.data['photos']:
            photos.append(Photo.objects.get(id=photo).file.url)
        share = ShareObject(user=user, url=url, share_time=share_time, photos=photos, folders=folders)
        mongo_result = share.save()
        print(mongo_result, type(mongo_result))

        shareauth = ShareAuthObject(url=url, ttl=ttl, password=password, mongoid=mongo_result.get("_id"))
        redis_result = shareauth.save()
        if not redis_result:
            Response(data={"status": "FAILURE", "message": "分享失败"}, status=status.HTTP_400_BAD_REQUEST)
        response_data = shareauth.serializer()
        return Response(data=response_data)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj:
            return Response(data="链接已失效")
        return Response(obj.serializer())

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        obj = self.get_object()
        photos = request.data['photos']
        folders = request.data['folders']
        if photos:
            obj.photos = []
            for photo in photos:
                obj.photos.append(Photo.objects.get(id=photo).file.url)
        if folders:
            obj.folders = folders
        serializer = obj.update()
        return Response(serializer)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        delete = obj.delete()
        return Response(data=delete, status=status.HTTP_204_NO_CONTENT)

    def get_object(self, queryset=None):
        # obj = rds.get(self.get_url()).decode().replace("'", "\"")
        obj = ShareObject.get(url=self.get_url())
        if not obj:
            return None
        return obj

    def get_url(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        url = self.kwargs[lookup_url_kwarg]
        return url


    # def get(self, request, url, format=None):
    #     data = json.loads(rds.get("django_test").decode().replace("'", "\""))
    #     return Response(data=data)
    #
    # def post(self, request, format=None):
    #     print(request.POST)
    #     # folders = request.POST['folders'].split(',')
    #     # photos = request.POST['photos'].split(',')
    #     # print(rds.set('django_test', ShareObject(self.request.user, "abc").serializer()))
    #
    #     return Response("ok")


class EditionViewSet(viewsets.GenericViewSet,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin, ):
    serializer_class = EditionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if user.is_staff == 0:
            return Response(data={"status": "FAILURE", "message": "请先登录"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        upload_time = datetime.now()
        apkFile = request.FILES['apkFile']
        changeLog = request.data['changeLog']
        editionCode = request.data['editionCode']
        url = "www.weasleyland.cn/media/edition/{}_{}".format(time(), apkFile.name)

        # photos = request.data['photos']
        # folders = []
        edition = EditionObject(user=user.id, upload_time=upload_time, apkFile=url, changeLog=changeLog, editionCode=editionCode)
        mongo_result = edition.save()
        if mongo_result.get('status') == "FAILURE":
            return Response(data={
                "status": "FAILURE",
                "msg": "版本号 {} 已存在".format(editionCode),
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        with open("media/edition/" + apkFile.name, 'wb') as file:
            file.write(apkFile.file.read())
        file.close()

        response_data = edition.serializer()
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj:
            return Response(data="版本失效")
        return Response(obj.serializer())

    def get_object(self, queryset=None):
        # obj = rds.get(self.get_url()).decode().replace("'", "\"")
        obj = EditionObject.get(editionCode=self.get_url())
        if not obj:
            return None
        return obj

    def get_url(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        url = self.kwargs[lookup_url_kwarg]
        return url
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


