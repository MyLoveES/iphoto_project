import base64
from urllib.parse import urlencode
from aip import AipFace

APP_ID = '11364785'
API_KEY = 'R7UGpOA0yuOpqrot6A790zqb'
SECRET_KEY = 'ME7HFLBPB9AGa7HyKpHV2emPRcT9o9Yc'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)
# str(base64.b64encode(open('1.jpg', 'rb').read()), 'utf-8')


class FaceAPI(object):
    client = client

    def face_detect(self, img, imageType):
        image = str(base64.b64encode(img), 'utf-8')
        # image = str(base64.b64encode(img.read()), 'utf-8')
        imageType = imageType
        """ 如果有可选参数 """
        options = {}
        options["face_field"] = "quality"
        options["face_type"] = "LIVE"

        """ 带参数调用人脸检测 """
        result = client.detect(image, imageType, options)
        print("detect_result:", result)
        # print(result.get('result').get('face_list')[0].get('face_token'))
        return {
            'status': True if not result.get('error_code') else False,
            'data': result
        }

    def face_search(self, img, imageType, groupIdList):
        # image = str(base64.b64encode(img.read()), 'utf-8')
        image = img
        imageType = imageType

        groupIdList = groupIdList

        """ 如果有可选参数 """
        options = {}
        options["liveness_control"] = "LOW"

        """ 带参数调用人脸搜索 """
        result = client.search(image, imageType, groupIdList, options)
        return {
            'status': True if not result.get('error_code') else False,
            'data': result
        }

    def face_add(self, image, imageType, groupId, userId):
        # image = str(base64.b64encode(image.read()), 'utf-8')
        image = image
        imageType = imageType

        groupId = groupId

        userId = userId
        """ 如果有可选参数 """
        options = {}
        # options["user_info"] = user_info

        """ 带参数调用人脸注册 """
        result = client.addUser(image, imageType, groupId, userId)
        return {
            'status': True if not result.get('error_code') else False,
            'data': result
        }

    def face_delete(self, userId, groupId, faceToken):
        userId = userId

        groupId = groupId

        faceToken = faceToken

        """ 调用人脸删除 """
        result = client.faceDelete(userId, groupId, faceToken)
        return {
            'status': True if not result.get('error_code') else False,
            'data': result
        }

    def face_match(self):
        result = client.match([
            {
                'image': base64.b64encode(open('1.jpg', 'rb').read()),
                'image_type': 'BASE64',
            },
            {
                'image': base64.b64encode(open('2.jpg', 'rb').read()),
                'image_type': 'BASE64',
            }
        ])

    def create_user_group(self, groupId):
        result = client.groupAdd(groupId)
        return {
            'status': True if not result.get('error_code') else False,
            'data': result
        }

    def get_user_list(self, groupId):
        groupId = groupId

        """ 调用获取用户列表 """
        result = client.getGroupUsers(groupId)
        # print(int(result.get('result').get('user_id_list')[-1])+1)
        return {
            'status': True if not result.get('error_code') else False,
            'data': result
        }


if __name__ == '__main__':
    face = FaceAPI()
    face.get_user_list('lrspc')
    # with open('8.jpg', 'rb') as file:
    #     print(face.face_search(str(base64.b64encode(open('7.jpeg', 'rb').read()), 'utf-8'), "BASE64", "wer"))

    # BASE64
    # result = client.match([
    #     {
    #         'image': str(base64.b64encode(open('7.jpeg', 'rb').read()), 'utf-8'),
    #         'image_type': 'BASE64',
    #     },
    #     {
    #         'image': str(base64.b64encode(open('2.jpg', 'rb').read()), 'utf-8'),
    #         'image_type': 'BASE64',
    #     }
    # ])
    # print(result)

    # URL
    # result = client.match([
    #     {
    #         'image': 'http://www.weasleyland.cn/media/photos/user_7/1528357376.7258337_1.jpg',
    #         'image_type': 'URL',
    #     },
    #     {
    #         'image': 'http://www.weasleyland.cn/media/photos/user_7/1528357414.2235253_2.jpg',
    #         'image_type': 'URL',
    #     }
    # ])
    # print(result)
    pass
