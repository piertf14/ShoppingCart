# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Course, Purchase
# Register your models here.


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'creation_date', 'active', )
    search_fields = ['name', 'image', 'creation_date', 'active', ]
    list_filter = ('active',)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'quantity', 'creation_date', )
    search_fields = ['user__username', 'course__name', ]