# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        if instance.first_name is None:
            instance.first_name = instance.username
        instance.save()
