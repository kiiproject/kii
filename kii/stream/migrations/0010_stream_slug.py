# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kii.base_models.fields


def set_stream_slug(apps, schema_editor):

    stream_model = apps.get_model("stream", "Stream")
    for stream in stream_model.objects.all():
        stream.slug = stream.title
        stream.save()


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0009_auto_20150104_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='slug',
            field=kii.base_models.fields.SlugField(populate_from=('title',), null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.RunPython(set_stream_slug),
    ]
