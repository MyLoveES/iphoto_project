from django.db import models
from photo.models import Photo
# Create your models here.
from django.conf import settings


class Album(models.Model):
    ALBUM_STATUS = (
        ("normal", "正常"),
        ("recycler", "回收站"),
        ("deleted", "彻底删除"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='album_user', on_delete=models.CASCADE, verbose_name='创建者')
    description = models.TextField(verbose_name='相册描述', null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='名称')
    upload_time = models.DateTimeField(auto_now=True, verbose_name='相册修改日期')
    status = models.CharField(default="normal", max_length=10, verbose_name='相册状态', choices=ALBUM_STATUS)
    photos = models.ManyToManyField(Photo, through='AlbumPhotoShip', through_fields=('album', 'photo'))
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='AlbumMemberShip', through_fields=('album', 'member'))

    class Meta:
        verbose_name = '相册'
        verbose_name_plural = '相册'
        unique_together = ('user', 'name')

    def __str__(self):
        return '{}/{}'.format(self.user.username, self.name)


class AlbumMemberShip(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='albummembership_member', on_delete=models.CASCADE, verbose_name='相册成员')
    album = models.ForeignKey(Album, related_name='albummembership_album', on_delete=models.CASCADE, verbose_name='相册')
    invite_time = models.DateTimeField(auto_now_add=True, verbose_name='相册成员邀请日期')
    inviter = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='albummembership_invites', verbose_name='相册成员邀请者')

    class Meta:
        verbose_name = '相册-用户关系表'
        verbose_name_plural = '相册-用户关系表'
        unique_together = ('album', 'member')


class AlbumPhotoShip(models.Model):
    photo = models.ForeignKey(Photo, related_name='albumphotoship_photo', on_delete=models.CASCADE, verbose_name='相册照片')
    album = models.ForeignKey('Album', related_name='albumphotoship_album', on_delete=models.CASCADE, verbose_name='相册')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='相册照片添加日期')
    adder = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE,
                              related_name='albumphotoship_adder', verbose_name='相册照片添加者')

    class Meta:
        verbose_name = '相册-照片关系表'
        verbose_name_plural = '相册-照片关系表'
        unique_together = ('album', 'photo')

# class AlbumUserRelation(models.Model):
#     RELATION_STATUS = (
#         (1, "成员"),
#         (2, "非成员"),
#     )
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='AlbumUserRelation_user', on_delete=models.CASCADE, verbose_name='用户')
#     album = models.ForeignKey(Album, related_name='AlbumUserRelation_album', verbose_name='相册', on_delete=models.CASCADE)
#     relation_time = models.DateTimeField(auto_now=True, verbose_name='用户关联日期')
#     status = models.IntegerField(default=1, verbose_name='关联状态', choices=RELATION_STATUS)
#
#     class Meta:
#         verbose_name = '相册-用户关系表'
#         verbose_name_plural = '相册-用户关系表'
#
#     def __str__(self):
#         return '{}-{}'.format(self.album, self.user)
#
#
# class AlbumPhotoRelation(models.Model):
#     RELATION_STATUS = (
#         (1, "成员"),
#         (2, "非成员"),
#     )
#     album = models.ForeignKey(Album, related_name='AlbumPhotoRelation_album', verbose_name='相册', on_delete=models.CASCADE)
#     photo = models.ForeignKey(Photo, related_name='AlbumPhotoRelation_photo', verbose_name='照片', on_delete=models.CASCADE)
#     relation_time = models.DateTimeField(auto_now=True, verbose_name='照片添加日期')
#     status = models.IntegerField(default=1, verbose_name='关联状态', choices=RELATION_STATUS)
#
#     class Meta:
#         verbose_name = '相册-照片关系表'
#         verbose_name_plural = '相册-照片关系表'
#
#     def __str__(self):
#         return '{}-{}'.format(self.album, self.photo)
