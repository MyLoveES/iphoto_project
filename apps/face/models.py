from django.db import models
# Create your models here.
from django.conf import settings

from photo.models import Photo


class Face(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='face_user', on_delete=models.CASCADE,
                             verbose_name='所属用户')
    face = models.CharField(max_length=100, null=False, blank=False, verbose_name="脸的标识", unique=True)

    class Meta:
        verbose_name = '人脸'
        verbose_name_plural = '人脸'

    def __str__(self):
        return '{}/{}'.format(self.user.username, self.face)


class FaceFile(models.Model):
    photo = models.OneToOneField(Photo, related_name='facefile_photo', on_delete=models.CASCADE,
                                 verbose_name='照片', unique=True)
    face = models.ForeignKey(Face, related_name='facefile_face', on_delete=models.CASCADE,
                             verbose_name='脸')

    class Meta:
        verbose_name = '人脸文件'
        verbose_name_plural = '人脸文件'

    def __str__(self):
        return '{}/{}'.format(self.face, self.photo)
