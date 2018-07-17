# Generated by Django 2.0.5 on 2018-06-16 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0002_auto_20180614_0705'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='is_character',
            new_name='is_person',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='is_book',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='is_cartoon',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='is_scenic',
        ),
        migrations.AddField(
            model_name='photo',
            name='is_animal',
            field=models.BooleanField(default=False, verbose_name='动物'),
        ),
        migrations.AddField(
            model_name='photo',
            name='is_export',
            field=models.BooleanField(default=False, verbose_name='体育'),
        ),
        migrations.AddField(
            model_name='photo',
            name='is_face',
            field=models.BooleanField(default=False, verbose_name='人脸'),
        ),
        migrations.AddField(
            model_name='photo',
            name='is_furniture',
            field=models.BooleanField(default=False, verbose_name='家居'),
        ),
        migrations.AddField(
            model_name='photo',
            name='is_gourmet',
            field=models.BooleanField(default=False, verbose_name='美食'),
        ),
        migrations.AddField(
            model_name='photo',
            name='is_office',
            field=models.BooleanField(default=False, verbose_name='办公'),
        ),
        migrations.AddField(
            model_name='photo',
            name='is_transport',
            field=models.BooleanField(default=False, verbose_name='交通'),
        ),
    ]