# -*- coding: utf-8 -*-

from django.contrib import admin
from facebookconnect.models import *


class FacebookProfileAdmin(admin.ModelAdmin):
    list_display = ('contrib_user','facebook_id')
admin.site.register(FacebookUser,FacebookProfileAdmin)


