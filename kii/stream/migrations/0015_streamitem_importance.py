# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0014_auto_20150118_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamitem',
            name='importance',
            field=models.IntegerField(choices=[(1, 'base_models.importance.low'), (2, 'base_models.importance.normal'), (3, 'base_models.importance.high')], default=2),
            preserve_default=True,
        ),
    ]
