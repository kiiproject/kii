# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='_content_rendered',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stream',
            name='content_markup_type',
            field=models.CharField(default='markdown', max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='streamitem',
            name='_content_rendered',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='streamitem',
            name='content_markup_type',
            field=models.CharField(default='markdown', max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='streamitemcomment',
            name='_content_rendered',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='streamitemcomment',
            name='content_markup_type',
            field=models.CharField(default='markdown', max_length=255),
            preserve_default=True,
        ),
    ]
