from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from face.models import Face, FaceFile
from util.encryption import make_share_url, make_face_token
from util.faceapi.Aipface import FaceAPI
# Create your views here.
from rest_framework import viewsets, mixins, filters

from face.serializers import FaceSerializer, FaceFileSerializer


# class FaceViewSets(viewsets.GenericViewSet,
#                    mixins.CreateModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.DestroyModelMixin, ):
#
#     serializer_class = FaceSerializer
#
#     def create(self, request, *args, **kwargs):
#         # try:
#             face_client = FaceAPI()
#
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             img = request.FILES['image']
#
#             detect_result = face_client.face_detect(img=img, imageType="BASE64")
#             if detect_result.get('status'):
#                 # user_info = request.data['user_info']
#                 groupIdList = request.data['machine_code']
#                 face_token = detect_result.get('data').get('result').get('face_list')[0].get('face_token')
#
#                 search_result = face_client.face_search(face_token, 'FACE_TOKEN', groupIdList)
#                 if search_result.get('status'):
#                     groupId = search_result.get('data').get('result').get('user_list')[0].get('group_id')
#                     userId = search_result.get('data').get('result').get('user_list')[0].get('user_id')
#                     score = search_result.get('data').get('result').get('user_list')[0].get('score')
#                     if score >= 80:
#                         add_result = face_client.face_add(image=face_token,
#                                                           imageType="FACE_TOKEN",
#                                                           groupId=groupId,
#                                                           userId=userId)
#                         response_data = {
#                             "catogary": "face",
#                             "message": {"group_id": groupId,
#                                         "userID": userId,
#                                         "face_token": face_token,
#                                         "score": score}
#                         }
#                         return Response(data=response_data)
#                     else:
#                         userId = int(face_client.get_user_list(groupId=groupId).get('data').get('result').get('user_id_list')[-1]) + 1 # 此处应为新的userID
#                         add_result = face_client.face_add(image=face_token,
#                                                           imageType="FACE_TOKEN",
#                                                           groupId=groupId,
#                                                           userId=userId)
#                         response_data = {
#                             "catogary": "face",
#                             "message": {"group_id": groupId,
#                                         "userID": userId,
#                                         "face_token": face_token,
#                                         "score": None}
#                         }
#                         return Response(data=response_data)
#                 else:
#                     face_client.create_user_group(groupId=groupIdList)
#                     userId = 0  # 此处应为新的userID
#                     add_result = face_client.face_add(image=face_token,
#                                                       imageType="FACE_TOKEN",
#                                                       groupId=groupIdList,
#                                                       userId=userId)
#                     response_data = {
#                         "catogary": "face",
#                         "message": {"group_id": groupIdList,
#                                     "userID": userId,
#                                     "face_token": face_token,
#                                     "score": None}
#                     }
#                     return Response(data=response_data)
#             else:
#                 return Response(data={"catogary": "entity", "message": "实体信息待定"})
#         #
#         # except Exception as e:
#         #     Response(data={'status': False, 'message': "GG"})


class FaceViewSet(viewsets.ModelViewSet):
    """
    Face view
    人脸 视图
    """
    queryset = Face.objects.all()
    serializer_class = FaceSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def create(self, request, *args, **kwargs):
        # 创建人脸
        times = 0
        while True:
            times = times + 1
            face_token = make_face_token()
            if not Face.objects.filter(face=face_token).exists():
                break
            if times >= 5:
                return Response({"msg": "创建失败，请重试"})
        request.data.__setitem__("face", face_token)
        return super(FaceViewSet, self).create(request, *args, **kwargs)


class FaceFileViewSet(viewsets.ModelViewSet):
    """
    FaceFile view
    人脸文件 视图
    """
    queryset = FaceFile.objects.all()
    serializer_class = FaceFileSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
