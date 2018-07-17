from enum import Enum, unique

from django.db.models import Q

from user.models import UserProfile
from photo.models import Photo
from folder.models import Folder
from album.models import Album


@unique
class ModelEnum(Enum):
    user = UserProfile,
    photo = Photo,
    folder = Folder,
    album = Album,


def check_owner(user, obj, model):
    if model.objects.filter(Q(user=user), Q(id=obj)):
        return True
    else:
        return False
