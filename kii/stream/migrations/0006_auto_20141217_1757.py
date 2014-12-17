# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0005_auto_20141217_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcomment',
            name='status',
            field=models.CharField(default='pub', max_length=5, choices=[('dra', 'base_models.status_mixin.draft'), ('pub', 'base_models.status_mixin.published')]),
        ),
        migrations.AlterField(
            model_name='streamitem',
            name='status',
            field=models.CharField(default='pub', max_length=5, choices=[('dra', 'base_models.status_mixin.draft'), ('pub', 'base_models.status_mixin.published')]),
        ),
    ]
