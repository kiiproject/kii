# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0014_auto_20150118_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('streamitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='stream.StreamItem')),
                ('file_obj', models.FileField(upload_to=b'kii/file/%Y/%m/%d')),
            ],
            options={
                'abstract': False,
            },
            bases=('stream.streamitem',),
        ),
    ]
