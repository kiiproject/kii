# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0002_file_mimetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='original_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
