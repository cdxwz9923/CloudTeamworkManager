import xadmin
from .models import *
from django import views

class personal_commentAdmin(object):
    search_fields = ['detail','id']
    list_filter = ['detail','id']
    list_display = ['detail','id']

# xadmin.site.register(personal_comment,personal_commentAdmin)


class personal_progressAdmin(object):
    list_display = ['detail','id']
    search_fields = ['detail','id']
    list_filter = ['detail','id']

# xadmin.site.register(personal_comment,personal_commentAdmin)


class personal_scheduleAdmin(models.Model):
    list_display = ['detail','id']
    list_filter = ['detail','id']
    search_fields = ['detail','id']

# xadmin.site.register(personal_comment,personal_commentAdmin)

