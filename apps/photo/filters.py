# -*- coding: utf-8 -*-
__author__ = 'bobby'

import django_filters
from django.db.models import Q
from photo.models import Photo, PhotoEntity, Category, Entity


class PhotoFilter(django_filters.rest_framework.FilterSet):
    """
    照片的过滤类
    """
    upload_time = django_filters.DateTimeFilter(name='upload_time', help_text="照片上传时间")
    # user_phone = django_filters.CharFilter(name='users', help_text='手机号', method='search_for_user')
    name = django_filters.CharFilter(name='name', help_text='照片名称', lookup_expr='contains')
    # android = django_filters.CharFilter(help_text='安卓种类', method='android_categery')
    categery = django_filters.CharFilter(help_text='种类', method='search_categery')
    entity = django_filters.CharFilter(help_text='实体', method='search_entity')
    user = django_filters.CharFilter(help_text='用户', method='search_user')
    # photo_user = django_filters.ModelChoiceFilter(queryset=UserModel.objects.all())
    # top_category = django_filters.NumberFilter(method='top_category_filter')

    def search_user(self, queryset, name, value):
        photo_set = queryset.filter(folder__user__username__contains=value)
        # photo_set = PhotoEntity.objects.filter(entity__entity__exact=value).values_list('photo')
        return photo_set

    def search_entity(self, queryset, name, value):
        # category_id = Category.objects.filter(category=value).first().id
        photo_set = queryset.filter(photoentity_photo__entity__entity__contains=value)
        # photo_set = PhotoEntity.objects.filter(entity__entity__exact=value).values_list('photo')
        return photo_set

    def search_categery(self, queryset, name, value):
        # category_id = Category.objects.filter(category=value).first().id
        # entity_set = Entity.objects.filter(category=category_id)
        # photo_set = PhotoEntity.objects.filter(entity__in=entity_set).values_list('photo').order_by('photo_id')
        photo_set = queryset.filter(photoentity_photo__entity__category__category__contains=value).distinct()
        return photo_set

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
        model = Photo
        fields = ['name', 'upload_time']
