# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0013_auto_20150107_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamitem',
            name='importance',
            field=models.IntegerField(default=2, choices=[(1, 'base_models.importance.low'), (2, 'base_models.importance.normal'), (3, 'base_models.importance.high')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='streamitem',
            name='root',
            field=models.ForeignKey(verbose_name='stream', to='stream.Stream', related_name='children'),
        ),
    ]
