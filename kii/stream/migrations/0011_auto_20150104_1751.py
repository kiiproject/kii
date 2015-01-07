# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kii.base_models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0010_stream_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='slug',
            field=kii.base_models.fields.SlugField(editable=False, populate_from=('title',), null=True, unique=True),
        ),
    ]
