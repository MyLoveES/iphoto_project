# Generated by Django 2.0.5 on 2018-06-05 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cloud',
            field=models.BooleanField(default=False, verbose_name='云空间开启状态'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.CharField(choices=[('active', '活跃'), ('logout', '注销'), ('banned', '封禁')], default='active', max_length=10, verbose_name='账户状态'),
        ),
    ]