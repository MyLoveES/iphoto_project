#!/usr/bin/env python
# encoding: utf-8

import xadmin
from xadmin import views
from user.models import UserProfile


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "iphoto"
    site_footer = "HOUTOU"


class UserAdmin(object):
    # list_display = '__all__'
    # search_fields = ['phnum', 'name']
    # list_editable = '__all__'
    # list_filter = '__all__'
    list_display = ['id',  "username", 'first_name', "email", "status"]
    search_fields = ['username', 'first_name',]
    list_editable = ["password", "username", 'first_name', "email", "status"]
    list_filter = ['id', "password", "username", 'first_name', "email", "status"]
    # style_fields = {"goods_desc": "ueditor"}
    # class GoodsImagesInline(object):
    #     model = UserModel
    #     exclude = ["add_time"]
    #     extra = 1
    #     style = 'tab'
    #
    # inlines = [GoodsImagesInline]


# class GoodsCategoryAdmin(object):
#     list_display = ["name", "category_type", "parent_category", "add_time"]
#     list_filter = ["category_type", "parent_category", "name"]
#     search_fields = ['name', ]
#
#
# class GoodsBrandAdmin(object):
#     list_display = ["category", "image", "name", "desc"]
#
#     def get_context(self):
#         context = super(GoodsBrandAdmin, self).get_context()
#         if 'form' in context:
#             context['form'].fields['category'].queryset = GoodsCategory.objects.filter(category_type=1)
#         return context
#
#
# class BannerGoodsAdmin(object):
#     list_display = ["goods", "image", "index"]
#
#
# class HotSearchAdmin(object):
#     list_display = ["keywords", "index", "add_time"]
#
#
# class IndexAdAdmin(object):
#     list_display = ["category", "goods"]
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UserAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

#
# xadmin.site.register(UserProfile, UserAdmin)
# xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
# xadmin.site.register(Banner, BannerGoodsAdmin)
# xadmin.site.register(GoodsCategoryBrand, GoodsBrandAdmin)
#
# xadmin.site.register(HotSearchWords, HotSearchAdmin)
# xadmin.site.register(IndexAd, IndexAdAdmin)

