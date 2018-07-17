import random
import string

from django.db import models
import time
from folder.models import Folder
from django.conf import settings


def photo_storage_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    storage_path = 'photos/user_{}/{}_{}'.format(instance.folder.user.id, time.time(), instance.file.name)
    return storage_path


class Photo(models.Model):
    PHOTO_STATUS = (
        ("normal", "正常"),
        ("recycler", "回收站"),
        ("deleted", "彻底删除"),
    )
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_related_photos',
    # on_delete=models.CASCADE, verbose_name='所属用户')
    folder = models.ForeignKey(Folder, related_name='photo_folder', on_delete=models.CASCADE, verbose_name='所属文件夹')
    # albums = models.ManyToManyField(Album, related_name='photo_album')
    # photo_top_category = models.CharField(max_length=12)
    # photo_secondary_category = models.CharField(max_length=12)
    name = models.CharField(max_length=100, verbose_name='名称')
    path = models.CharField(max_length=200, blank=True, null=True, verbose_name='Android路径')
    upload_time = models.DateTimeField(auto_now=True, verbose_name='照片上传日期')
    upload_place = models.CharField(max_length=20, null=True, blank=True, default='Default Place')
    status = models.CharField(default="normal", max_length=10, verbose_name='照片状态', choices=PHOTO_STATUS)
    description = models.TextField(verbose_name='照片描述', null=True, blank=True)
    selected_times = models.IntegerField(default=0, verbose_name='照片选择次数', null=True, blank=True)
    file = models.FileField(upload_to=photo_storage_path, verbose_name='照片路径')

    class Meta:
        verbose_name = '照片'
        verbose_name_plural = '照片'

    def __str__(self):
        return self.file.name


class Category(models.Model):
    category = models.CharField(max_length=10, blank=False, null=False, verbose_name='种类', unique=True)

    class Meta:
        verbose_name = '种类'
        verbose_name_plural = '种类'

    def __str__(self):
        return self.category


# class Entity(models.Model):
#     entity = models.CharField(max_length=10, blank=False, null=False, verbose_name='实体')
#
#     class Meta:
#         verbose_name = '实体'
#         verbose_name_plural = '实体'
#
#     def __str__(self):
#         return self.entity


class Entity(models.Model):
    category = models.ForeignKey(Category, related_name='entity_category', on_delete=models.CASCADE, verbose_name='种类')
    entity = models.CharField(max_length=20, blank=False, null=False, verbose_name='实体', unique=True)

    class Meta:
        verbose_name = '实体'
        verbose_name_plural = '实体'

    def __str__(self):
        return '{}/{}'.format(self.category.category, self.entity)


class PhotoEntity(models.Model):
    entity = models.ForeignKey(Entity, related_name='photoentity_entity', on_delete=models.CASCADE, verbose_name='实体')
    photo = models.ForeignKey(Photo, related_name='photoentity_photo', on_delete=models.CASCADE, verbose_name='照片')

    class Meta:
        verbose_name = '照片实体关系'
        verbose_name_plural = '照片实体关系'
        unique_together = ('entity', 'photo')

    def __str__(self):
        return '{}/{}/{}'.format(self.photo.folder.user.username, self.photo.name, self.entity)
