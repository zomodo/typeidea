# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-02-14 10:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='link',
            options={'ordering': ['-weight'], 'verbose_name': '友链', 'verbose_name_plural': '友链'},
        ),
    ]