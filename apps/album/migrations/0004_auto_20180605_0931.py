# Generated by Django 2.0.5 on 2018-06-05 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0003_auto_20180605_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='status',
            field=models.CharField(choices=[('normal', '正常'), ('recycle', '回收站'), ('deleted', '彻底删除')], default='normal', max_length=10, verbose_name='相册状态'),
        ),
    ]
