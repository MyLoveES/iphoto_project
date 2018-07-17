"""iphoto_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import xadmin
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework.schemas import get_schema_view
from django.conf.urls import url, include
# from django.contrib import admin
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from django.urls import path, re_path

# from face.views import FaceViewSets
from face.views import FaceViewSet, FaceFileViewSet
from operation.views import ShareOperationViewSet, EditionViewSet
from user.views import UsersViewSet, SmsCodeViewset
from folder.views import FolderViewSet
from photo.views import PhotoViewSet, CategoryViewSet, EntityViewSet, PhotoEntityViewSet
from album.views import AlbumViewSet, AlbumMemberInvitationViewSet, AlbumPhotoAdderViewSet
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
# from django.conf.urls.static import static
# from django.conf import settings
schema_view = get_schema_view(title='Pastebin API')
router = DefaultRouter()
# router.register('register', UsersRegisterViewSet, base_name='register')
# router.register('login', UsersLoginViewSet, base_name='login')
# router.register('upload', UsersLoginViewSet, base_name='upload')
router.register('users', UsersViewSet, base_name='user')

router.register('folders', FolderViewSet, base_name='folder')

router.register('photos', PhotoViewSet, base_name='photo')
router.register('category', CategoryViewSet, base_name='category')
router.register('entity', EntityViewSet, base_name='entity')
router.register('photoentity', PhotoEntityViewSet, base_name='photoentity')

router.register('albums', AlbumViewSet, base_name='album')
router.register('invite', AlbumMemberInvitationViewSet, base_name='albummembership')
router.register('add', AlbumPhotoAdderViewSet, base_name='albumphotoship')

router.register('code', SmsCodeViewset, base_name='code')
router.register('share', ShareOperationViewSet, base_name='shareoperation'),
router.register('face', FaceViewSet, base_name='face'),
router.register('facefile', FaceFileViewSet, base_name='facefile'),
router.register('edition', EditionViewSet, base_name='edition'),

urlpatterns = [
    url(r'^schema/$', schema_view),
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('docs/', include_docs_urls(title="docs")),
    path('', include(router.urls)),
    # path('users/', include('user.urls')),
    # path('photos/', include('photo.urls')),
    # path('folders/', include('folder.urls')),
    re_path('jwt_login/', obtain_jwt_token),
    path('login_refresh/', refresh_jwt_token),
    path('', include('social_django.urls', namespace='social'))
    # path('share/<int:question_id>/', views.vote, name='vote'),
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Login and logout views for the browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
