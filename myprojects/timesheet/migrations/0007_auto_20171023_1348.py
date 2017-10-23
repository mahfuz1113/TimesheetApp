# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 05:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0006_auto_20171023_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheet',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
    ]
