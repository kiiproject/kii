# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='mimetype',
            field=models.CharField(default='text/plain', max_length=255),
            preserve_default=False,
        ),
    ]
