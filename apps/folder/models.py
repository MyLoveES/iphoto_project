# Create your models here.


from django.db import models
import time
from django.conf import settings


class Folder(models.Model):
    FOLDER_STATUS = (
        ("normal", "正常"),
        ("recycler", "回收站"),
        ("deleted", "彻底删除"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='folder_user', on_delete=models.CASCADE, verbose_name='所属用户')
    name = models.CharField(max_length=100, verbose_name='名称')
    upload_time = models.DateTimeField(auto_now=True, verbose_name='文件夹修改日期')
    status = models.CharField(default="normal", max_length=10, verbose_name='文件夹状态', choices=FOLDER_STATUS)

    class Meta:
        verbose_name = '文件夹'
        verbose_name_plural = '文件夹'
        unique_together = ("user", "name")

    def __str__(self):
        return '{}/{}'.format(self.user.username, self.name)
