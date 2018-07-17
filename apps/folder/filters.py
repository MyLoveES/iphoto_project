# -*- coding: utf-8 -*-
__author__ = 'bobby'

import django_filters
from django.db.models import Q
from folder.models import Folder


class FolderFilter(django_filters.rest_framework.FilterSet):
    """
    相册的过滤类
    """
    upload_time = django_filters.DateTimeFilter(name='upload_time', help_text="文件夹上传时间")
    name = django_filters.CharFilter(name='name', help_text='相册名称', lookup_expr='contains')
    # photo_user = django_filters.ModelChoiceFilter(queryset=UserModel.objects.all())
    # top_category = django_filters.NumberFilter(method='top_category_filter')

    # def search_files(self, queryset, name, value):
    #     file_queryset = queryset.filter(path__exact=value)
    #     return file_queryset
    #
    # def search_for_user(self, queryset, name, value):
    #     file_queryset = queryset.filter(user__phnum__contains=value)
    #     return file_queryset
        # result_set = []
        # photo_queryset = queryset.select_related('photo_user')
        # for qs in photo_queryset:
        #     if value in qs.photo_user.user_phnum:
        #         result_set.append(qs)
        # return result_set
        # user_queryset = User.objects.filter(user_phnum=value)
        # if user_queryset and user_queryset.filter():
        #     photo_queryset = queryset.fileter(photo_user=user_queryset.get)

    class Meta:
        model = Folder
        fields = ['user', 'name', 'upload_time', 'status']
