from django.conf.urls import url
from rest_framework.schemas import get_schema_view
from django.conf.urls import url, include
# from django.contrib import admin
import xadmin
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from django.urls import path
from folder import views

schema_view = get_schema_view(title='Pastebin API')
router = DefaultRouter()
# Create a router and register our viewsets with it.
router.register('', views.FolderViewSet)
# router.register('op', views.FolderOperateViewSet, base_name='op')
# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('schema/', schema_view),
    # path('list/', PhotoListView.as_view()),
    path('', include(router.urls)),
]