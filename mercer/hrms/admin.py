# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.
class NewUserAdmin(admin.ModelAdmin):
	list_display = ('username','date_joined', 'profile')

admin.site.register(NewUser, NewUserAdmin)
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Rank)