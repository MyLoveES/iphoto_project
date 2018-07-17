# Create your models here.
from django.db import models
from datetime import datetime
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.contrib.auth.models import AbstractUser
# LEXERS = [item for item in get_all_lexers() if item[1]]
# LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
# STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class UserProfile(AbstractUser):
    USER_STATUS = (
        ("active", "活跃"),
        ("logout", "注销"),
        ("banned", "封禁"),
    )

    # phone = models.CharField(max_length=12, unique=True, verbose_name='用户手机号')
    # cloud = models.BooleanField(default=False, verbose_name='云空间开启状态')
    status = models.CharField(default="active", max_length=10, verbose_name='账户状态', choices=USER_STATUS)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.first_name

