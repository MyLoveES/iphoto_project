#!/usr/bin/env python
# encoding: utf-8

import xadmin
# from operation.models import AlbumPhotoShip, AlbumMemberShip
#
#
# class AlbumMemberShipAdmin(object):
#     # list_display = '__all__'
#     # search_fields = ['user', "name"]
#     # list_editable = '__all__'
#     # list_filter = '__all__'
#     list_display = ['id', "member", "album", "invite_time", "inviter"]
#     search_fields = ["album", "member"]
#     list_editable = ["member", "album", "invite_time", "inviter"]
#     list_filter = ["member", "album", "invite_time", "inviter"]
#     # style_fields = {"goods_desc": "ueditor"}
#     # class GoodsImagesInline(object):
#     #     model = User
#     #     exclude = ["add_time"]
#     #     extra = 1
#     #     style = 'tab'
#     #
#     # inlines = [GoodsImagesInline]
#
#
# class AlbumPhotoShipAdmin(object):
#     # list_display = '__all__'
#     # search_fields = ['user', "name"]
#     # list_editable = '__all__'
#     # list_filter = '__all__'
#     list_display = ['id', "photo", "album", "add_time", "adder"]
#     search_fields = ["album", "photo"]
#     list_editable = ["photo", "album", "add_time", "adder"]
#     list_filter = ["photo", "album", "add_time", "adder"]
#
# xadmin.site.register(AlbumPhotoShip, AlbumPhotoShipAdmin)
# xadmin.site.register(AlbumMemberShip, AlbumMemberShipAdmin)
# class AlbumPhotoRelationAdmin(object):
#     list_display = ['id', "user", "album", "relation_time", "status"]
#     search_fields = ["user", "album"]
#     list_editable = ["user", "album", "relation_time", "status"]
#     list_filter = ["user", "album", "relation_time", "status"]
#
#
# class AlbumUserRelationAdmin(object):
#     list_display = ['id', "album", "photo", "relation_time", "status"]
#     search_fields = ["album", "photo"]
#     list_editable = ["album", "photo", "relation_time", "status"]
#     list_filter = ["album", "photo", "relation_time", "status"]
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


# xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
# xadmin.site.register(Banner, BannerGoodsAdmin)
# xadmin.site.register(GoodsCategoryBrand, GoodsBrandAdmin)
#
# xadmin.site.register(HotSearchWords, HotSearchAdmin)
# xadmin.site.register(IndexAd, IndexAdAdmin)

