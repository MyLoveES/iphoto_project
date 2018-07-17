#!/usr/bin/env python
# encoding: utf-8

import xadmin
from folder.models import Folder


class FolderAdmin(object):
    # list_display = '__all__'
    # search_fields = ['user', "name"]
    # list_editable = '__all__'
    # list_filter = '__all__'
    list_display = ['id', 'user', "name", "upload_time", "status",]
    search_fields = ['user', "name"]
    list_editable = ['user', "name", "upload_time", "status",]
    list_filter = ['user', "name", "upload_time", "status",]
    # style_fields = {"goods_desc": "ueditor"}
    # class GoodsImagesInline(object):
    #     model = User
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


# xadmin.site.unregister(User)
xadmin.site.register(Folder, FolderAdmin)
# xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
# xadmin.site.register(Banner, BannerGoodsAdmin)
# xadmin.site.register(GoodsCategoryBrand, GoodsBrandAdmin)
#
# xadmin.site.register(HotSearchWords, HotSearchAdmin)
# xadmin.site.register(IndexAd, IndexAdAdmin)

