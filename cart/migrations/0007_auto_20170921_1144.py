# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 16:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_course_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='cost',
            new_name='price',
        ),
    ]
