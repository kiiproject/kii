# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0013_auto_20150107_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamitem',
            name='root',
            field=models.ForeignKey(related_name='children', verbose_name='stream', to='stream.Stream'),
        ),
    ]
