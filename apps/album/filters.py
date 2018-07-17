# -*- coding: utf-8 -*-
__author__ = 'bobby'

import django_filters
from django.db.models import Q
from album.models import Album


class AlbumFilter(django_filters.rest_framework.FilterSet):
    """
    相册的过滤类
    """
    user = django_filters.CharFilter(name='user', help_text='相册创建者', method='search_user')
    description = django_filters.CharFilter(name='description', help_text='相册描述', lookup_expr="contains")
    status = django_filters.NumberFilter(name='status', help_text='相册状态')
    upload_time = django_filters.DateTimeFilter(name='upload_time', help_text="相册创建时间")
    # user_phone = django_filters.CharFilter(name='users', help_text='手机号', method='search_for_user')
    name = django_filters.CharFilter(name='name', help_text='相册名', lookup_expr="contains")
    # photo_user = django_filters.ModelChoiceFilter(queryset=UserModel.objects.all())
    # top_category = django_filters.NumberFilter(method='top_category_filter')
    # def search_for_user(self, queryset, name, value):
    #     file_queryset = queryset.filter(user__phnum__contains=value)
    #     return file_queryset
    #     result_set = []
    #     photo_queryset = queryset.select_related('photo_user')
    #     for qs in photo_queryset:
    #         if value in qs.photo_user.user_phnum:
    #             result_set.append(qs)
    #     return result_set
    #     user_queryset = User.objects.filter(user_phnum=value)
    #     if user_queryset and user_queryset.filter():
    #         photo_queryset = queryset.fileter(photo_user=user_queryset.get)

    def search_user(self, queryset, name, value):
        album_set = queryset.filter(user__username__contains=value)
        # photo_set = PhotoEntity.objects.filter(entity__entity__exact=value).values_list('photo')
        return album_set

    class Meta:
        model = Album
        fields = '__all__'

#
# class AlbumUserRelationFilter(django_filters.rest_framework.FilterSet):
#     """
#     相册-用户关联的过滤类
#     """
#     user = django_filters.CharFilter(name='user', help_text='用户')
#     album = django_filters.CharFilter(name='album', help_text='相册')
#     status = django_filters.NumberFilter(name='status', help_text='关联状态')
#     relation_time = django_filters.DateTimeFilter(name='upload_time', help_text="关联时间")
#     # user_phone = django_filters.CharFilter(name='users', help_text='手机号', method='search_for_user')
#     # photo_user = django_filters.ModelChoiceFilter(queryset=UserModel.objects.all())
#     # top_category = django_filters.NumberFilter(method='top_category_filter')
#     # def search_for_user(self, queryset, name, value):
#     #     file_queryset = queryset.filter(user__phnum__contains=value)
#     #     return file_queryset
#         # result_set = []
#         # photo_queryset = queryset.select_related('photo_user')
#         # for qs in photo_queryset:
#         #     if value in qs.photo_user.user_phnum:
#         #         result_set.append(qs)
#         # return result_set
#         # user_queryset = User.objects.filter(user_phnum=value)
#         # if user_queryset and user_queryset.filter():
#         #     photo_queryset = queryset.fileter(photo_user=user_queryset.get)
#
#     class Meta:
#         model = AlbumUserRelation
#         fields = '__all__'
#
#
# class AlbumPhotoRelationFilter(django_filters.rest_framework.FilterSet):
#     """
#     相册-照片关联的过滤类
#     """
#     photo = django_filters.CharFilter(name='photo', help_text='用户')
#     album = django_filters.CharFilter(name='album', help_text='相册')
#     status = django_filters.NumberFilter(name='status', help_text='关联状态')
#     relation_time = django_filters.DateTimeFilter(name='upload_time', help_text="关联时间")
#     # photo_user = django_filters.ModelChoiceFilter(queryset=UserModel.objects.all())
#     # top_category = django_filters.NumberFilter(method='top_category_filter')
#     # def search_for_user(self, queryset, name, value):
#     #     file_queryset = queryset.filter(user__phnum__contains=value)
#     #     return file_queryset
#         # result_set = []
#         # photo_queryset = queryset.select_related('photo_user')
#         # for qs in photo_queryset:
#         #     if value in qs.photo_user.user_phnum:
#         #         result_set.append(qs)
#         # return result_set
#         # user_queryset = User.objects.filter(user_phnum=value)
#         # if user_queryset and user_queryset.filter():
#         #     photo_queryset = queryset.fileter(photo_user=user_queryset.get)
#
#     class Meta:
#         model = AlbumPhotoRelation
#         fields = '__all__'
