# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='courses/')
    creation_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ('-creation_date',)

    def __unicode__(self):
        return '%s' % self.name


class Purchase(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    quantity = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)    

    class Meta:
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"
        ordering = ('-creation_date',)

    def __unicode__(self):
        return '%s' % self.id

    def total_price(self):
        return self.quantity * self.course.unit_price
    total_price = property(total_price)
