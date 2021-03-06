# Generated by Django 2.0.5 on 2018-06-16 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0003_auto_20180616_0643'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=10, verbose_name='种类')),
            ],
            options={
                'verbose_name': '种类',
                'verbose_name_plural': '种类',
            },
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity', models.CharField(max_length=10, verbose_name='实体')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categoryentity_category', to='photo.Category', verbose_name='种类')),
            ],
            options={
                'verbose_name': '实体',
                'verbose_name_plural': '实体',
            },
        ),
        migrations.RemoveField(
            model_name='photo',
            name='is_animal',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='is_export',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='is_face',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='is_furniture',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='is_gourmet',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='is_office',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='is_person',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='is_transport',
        ),
        migrations.AddField(
            model_name='photo',
            name='category',
            field=models.IntegerField(default=0, verbose_name='照片种类'),
        ),
    ]
