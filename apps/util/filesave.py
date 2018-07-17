from urllib import request

from photo.models import Photo

if __name__ == '__main__':
    # print('ok')
    # with open('filedownload.jpg', 'wb') as f:
    #     f.write(request.urlopen("http://www.weasleyland.cn/media/photos/user_7/1528116303.7386138_mmexport1528078358437.jpg").read())
    # f.close()
    print(type(Photo.objects.get(id=2400).file))
    pass