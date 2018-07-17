# Generated by Django 2.0.5 on 2018-06-14 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='status',
            field=models.CharField(choices=[('normal', '正常'), ('recycler', '回收站'), ('deleted', '彻底删除')], default='normal', max_length=10, verbose_name='照片状态'),
        ),
    ]