# Author : zmd
# Date : 2019/12/31 10:22
# Desc : 用户模块的管理和文章模块的管理分开

from django.contrib.admin import AdminSite

class CustomSite(AdminSite):
    site_header = 'Typeidea'
    site_title = 'Typeidea管理后台'
    index_title = '首页'

custom_site=CustomSite(name='cus_admin')