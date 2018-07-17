# Create your tasks here
from __future__ import absolute_import, unicode_literals

import base64

from celery import shared_task
from kombu import Queue
from pykafka import KafkaClient
import json
import requests
from aip import AipFace


from face.models import Face, FaceFile
from photo.models import Photo
from user.models import UserProfile
from util.encryption import make_face_token
from util.faceapi.Aipface import FaceAPI

APP_ID = '11364785'
API_KEY = 'R7UGpOA0yuOpqrot6A790zqb'
SECRET_KEY = 'ME7HFLBPB9AGa7HyKpHV2emPRcT9o9Yc'

face_api = FaceAPI()


def face_detect(photo):
    data = {
        "token".encode(): "qqwrv".encode(),
    }
    files = {'face': photo}
    url = "http://106.15.183.211:8000/judge_face/"
    response = requests.post(url, data=data, files=files)
    response_data = response.json()
    print(response.text)
    face_num = response_data.get('face_num')
    if face_num == 1:
        return "face"
    else:
        return "entity"


def face_detect_baidu(photo):
    result = face_api.face_detect(photo.file.open().read(), imageType="BASE64")
    print("detect result: ", result)
    if result.get('data').get('error_code') == 0:
        face_num = result.get('data').get('result').get('face_num')
        if face_num == 1:
            return "face"
        else:
            return "entity"
    else:
        return "entity"


def face_recognition(face1, face2):
    files = {'face1': face1,
             'face2': face2}

    data = {
        "token".encode(): "qqwrv".encode(),
    }
    # client = AipFace(APP_ID, API_KEY, SECRET_KEY)
    # result = client.match([
    #     {
    #         'image': str(base64.b64encode(face1), 'utf-8'),
    #         'image_type': 'BASE64',
    #     },
    #     {
    #         'image': str(base64.b64encode(face2), 'utf-8'),
    #         'image_type': 'BASE64',
    #     }
    # ])
    # print("baidu result: ", result)
    # url= "http://106.15.183.211:8000/judge_face/"
    url = "http://106.15.183.211:8000/two_face/"
    reponse = requests.post(url, data=data, files=files)
    print('EEEEEEEEEEEEsfag:', reponse.text)
    score = reponse.json().get('result')
    print("SSSSSSSSSSSSSSSSSSSSSore:", score)
    return score


def face_recognition_baidu(face1, face2):
    result = face_api.client.match([
        {
            'image': str(base64.b64encode(face1.file.open().read()), 'utf-8'),
            'image_type': 'BASE64',
        },
        {
            'image': str(base64.b64encode(face2.file.open().read()), 'utf-8'),
            'image_type': 'BASE64',
        }
    ])
    print("recognize result: ", result)
    if result.get('error_code') == 0:
        score = result.get('result').get('score')
        score = score/100
        return score
    else:
        return 0.6


@shared_task
def kafka_produce(kafka_message):
    print("task begin")
    photo_id = kafka_message.get('photo')
    print("photo_id:", photo_id)
    face_file_new = Photo.objects.filter(id=photo_id).first()
    # with face_file_new.file.open() as file1:
    #     photo = file1.read()
    #     file1.close()
    # face_detect_result = face_detect(photo)
    face_detect_result = face_detect_baidu(face_file_new)
    client = KafkaClient(hosts="106.15.191.61:9092")
    topic = client.topics["entity".encode()]
    last_offset = topic.latest_available_offsets()
    with topic.get_producer(delivery_reports=True) as producer:
        producer.produce(json.dumps(kafka_message).encode())
        # try:
        #     msg, exc = producer.get_delivery_report(block=False)
        #     if exc is not None:
        #         return 'Failed to deliver msg {}: {}'.format(msg.partition_key, repr(exc))
        #     else:
        #         return 'Successfully delivered msg {}'.format(msg.partition_key)
        # except Queue.Empty:
        #     return 'Queue Empty ERROR'
    print("face_detect_result:", face_detect_result)
    if face_detect_result == "face":
        face_score = {}
        user = UserProfile.objects.filter(id=kafka_message.get('user')).first()
        # face_path = kafka_message.get('photo_filepath')
        print('face_file_new:', face_file_new)
        face_queryset = Face.objects.filter(user=user)
        print('face_queryset :', face_queryset)
        if not face_queryset.exists():
            times = 0
            while True:
                times = times + 1
                face_token = make_face_token()
                if not Face.objects.filter(face=face_token).exists():
                    break
                if times >= 5:
                    return "人脸创建失败"
            new_face = Face(user=user, face=face_token)
            new_face.save()
            FaceFile(face=new_face, photo=face_file_new).save()
            return "人脸创建成功"
        for face in face_queryset:
            print('face:', face.face)
            file_score = []
            facefile_queryset = FaceFile.objects.filter(face=face)
            print('facefile_queryset:', facefile_queryset.exists())
            for face_file in facefile_queryset:
                face_file_old = face_file.photo
                print('face_file_old:', face_file_old.id)
                # with face_file_new.file.open() as file1:
                #     file_new = file1.read()
                #     file1.close()
                # with face_file_old.file.open() as file2:
                #     file_old = file2.read()
                #     file2.close()
                # score = face_recognition(file_new, file_old)
                score = face_recognition_baidu(face_file_new, face_file_old)
                print('score:', score)
                file_score.append(score)
            print('face_score:', face_score)
            face_score[face.face] = sum(file_score) / len(file_score) if len(file_score) != 0 else 0
            print('face_score[face.face]:', face_score[face.face])
        print('face_score:', face_score)
        face_score_tup_list = sorted(face_score.items(), key=lambda item: item[1], reverse=True)
        print('face_score_tup_list:', face_score_tup_list)
        face_score_tup = face_score_tup_list[0]
        face = face_score_tup[0]
        score = face_score_tup[1]
        if score > 0.6:
            FaceFile(face=face_queryset.filter(face=face).first(), photo=face_file_new).save()
        else:
            times = 0
            while True:
                times = times + 1
                face_token = make_face_token()
                if not Face.objects.filter(face=face_token).exists():
                    break
                if times >= 5:
                    return "人脸创建失败"
            new_face = Face(user=user, face=face_token)
            new_face.save()
            FaceFile(face=face_queryset.filter(face=new_face.face).first(), photo=face_file_new).save()
        return "人脸创建成功"
    else:
        return "物体识别"


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)