# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreamItemChild1',
            fields=[
                ('streamitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='stream.StreamItem')),
            ],
            options={
                'abstract': False,
            },
            bases=('stream.streamitem',),
        ),
        migrations.CreateModel(
            name='StreamItemChild2',
            fields=[
                ('streamitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='stream.StreamItem')),
            ],
            options={
                'abstract': False,
            },
            bases=('stream.streamitem',),
        ),
    ]
