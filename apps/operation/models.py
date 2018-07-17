from django.conf import settings
from django.db import models
# Create your models here.
from photo.models import Photo
from util.mongo_connect import collection, editionCollection

# class ShareObject(object):
#     user = None
#     password = None
#     folders = []
#     photos = []
#
#     def __init__(self, user, password, folders, photos):
#         self.user = user if type(user) is int else user.id
#         self.password = password
#         self.folders = folders
#         self.photos = photos
#
#     def serializer(self):
#         serializer_data = {
#             "user": self.user,
#             "password": self.password,
#             "folders": self.folders,
#             "photos": self.photos
#         }
#         return serializer_data
#
#     def save(self, url, ttl):
#         """
#         :param url: 神秘链接
#         :param ttl: 生存值
#         :argument ttl_choice: 生存时间选项,1:7days, 2:30days, 3:forever
#         :return: 分享本体
#         """
#         ttl_choice = {
#             1: 60*60*24*7,
#             2: 60*60*24*30,
#             3: -1
#         }
#         ttl = ttl_choice[ttl]
#         redis_data = self.serializer()
#         rds_for_share.set(name=url, value=redis_data, ex=ttl)
#         return redis_data
#
#     def delete(self, url):
#         return rds_for_share.delete(url)
from util.redis_connect import rds_for_share


class EditionObject(object):
    apkFile = None
    user = None
    upload_time = None
    editionCode = None
    changeLog = None

    def __init__(self, apkFile, user, upload_time, editionCode, changeLog, **kwargs):
        self.apkFile = apkFile
        self.user = user
        self.upload_time = upload_time
        self.editionCode = editionCode
        self.changeLog = changeLog

    def serializer(self):
        serializer_data = {
            "apkFile": self.apkFile,
            "user": self.user,
            "upload_time": self.upload_time,
            "editionCode": self.editionCode,
            "changeLog": self.changeLog,
        }
        return serializer_data

    def save(self):
        # ttl_choice = {
        #     0: 60,
        #     1: 60 * 60 * 24,
        #     2: 60 * 60 * 24 * 7,
        #     3: 60 * 60 * 24 * 30,
        #     4: -1
        # }
        # ttl = ttl_choice[self.ttl]
        data = self.serializer()
        if editionCollection.find_one(filter={"editionCode": data.get("editionCode")}) is not None:
            return {
                "status": "FAILURE",
                "msg": "EditionCode Exits"
            }
        editionCollection.insert(data)
        # if ttl is not -1:
        #     collection.create_index("share_time", expireAfterSeconds=ttl)
        return {
                "status": "SUCCESS",
                "data": data
            }

    @staticmethod
    def get(editionCode):
        data = editionCollection.find_one({"editionCode": editionCode})
        if data:
            return ShareObject(**data)
        else:
            return None

    def delete(self):
        return editionCollection.delete_one({"url": self.editionCode})

    def update(self):
        return editionCollection.update_one({"editionCode": self.editionCode}, {"$set": {"photos": self.photos, "folders": self.folders}})


class ShareObject(object):
    url = None
    user = None
    share_time = None
    folders = []
    photos = []

    def __init__(self, user, url, folders, photos, share_time, **kwargs):
        self.user = user if type(user) is int else user.id
        self.url = url
        self.share_time = share_time
        self.folders = folders
        self.photos = photos

    def serializer(self):
        serializer_data = {
            "user": self.user,
            "url": self.url,
            "folders": self.folders,
            "photos": self.photos,
            "share_time": self.share_time,
        }
        return serializer_data

    def save(self):
        # ttl_choice = {
        #     0: 60,
        #     1: 60 * 60 * 24,
        #     2: 60 * 60 * 24 * 7,
        #     3: 60 * 60 * 24 * 30,
        #     4: -1
        # }
        # ttl = ttl_choice[self.ttl]
        data = self.serializer()
        collection.insert(data)
        # if ttl is not -1:
        #     collection.create_index("share_time", expireAfterSeconds=ttl)
        return data

    @staticmethod
    def get(url):
        data = collection.find_one({"url": url})
        if data:
            return ShareObject(**data)
        else:
            return None

    def delete(self):
        return collection.delete_one({"url": self.url})

    def update(self):
        return collection.update_one({"url": self.url}, {"$set": {"photos": self.photos, "folders": self.folders}})


class ShareAuthObject(object):
    ttl = None
    url = None
    password = None
    mongoid = None

    def __init__(self, url, password, mongoid, ttl):
        self.ttl = ttl
        self.mongoid = str(mongoid)
        self.url = url
        self.password = password

    def save(self):
        #
        ttl_choice = {
            0: 60,
            1: 60 * 60 * 24,
            2: 60 * 60 * 24 * 7,
            3: 60 * 60 * 24 * 30,
            4: -1
        }
        key = self.url
        value = {
            "password": self.password,
            "mongoid": self.mongoid
        }
        ex = ttl_choice[self.ttl]
        print(value)
        return rds_for_share.set(name=key, value=value, ex=ex)

    @staticmethod
    def get(url):
        data = rds_for_share.get(url).decode()
        print(eval(data))
        return eval(data)

    def serializer(self):
        serializer_data = {
            "url": self.url,
            "password": self.password,
        }
        return serializer_data

#
# class ShareOperation(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='shareoperation_user', on_delete=models.CASCADE, verbose_name='分享者')
#     photo = models.ManyToManyField(Photo, related_name='shareoperation_photo', verbose_name='分享照片')
#     timeout = models.DateTimeField(auto_now_add=True)
#     url = models.CharField(unique=True)
#     key = models.CharField()
#
#     class Meta:
#         verbose_name = '用户分享'
#         verbose_name_plural = '用户分享'
#
#     def __str__(self):
#         return '{}/{}'.format(self.id, self.url)
