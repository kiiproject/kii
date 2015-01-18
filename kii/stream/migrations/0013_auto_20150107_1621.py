# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def fix_stream_slug(apps, schema_editor):
    """Populate empty stream slugs with title"""
    Stream = apps.get_model("stream", "Stream")

    streams = Stream.objects.filter(slug=None)

    for stream in streams:
        stream.slug = stream.title
        stream.save()

class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0012_auto_20150104_1752'),
    ]

    operations = [
        migrations.RunPython(fix_stream_slug),
    ]
