# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0006_auto_20141217_1757'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stream',
            options={'permissions': (('read', 'permissions.read'), ('write', 'permissions.write'), ('delete', 'permissions.delete'))},
        ),
        migrations.AlterModelOptions(
            name='streamitem',
            options={'ordering': ['-publication_date'], 'permissions': (('read', 'permissions.read'), ('write', 'permissions.write'), ('delete', 'permissions.delete'))},
        ),
        migrations.RemoveField(
            model_name='itemcomment',
            name='publication_date',
        ),
        migrations.AlterField(
            model_name='itemcomment',
            name='status',
            field=models.CharField(default='awaiting_moderation', max_length=255, choices=[('published', 'published'), ('awaiting_moderation', 'awaiting moderation'), ('disapproved', 'disapproved'), ('junk', 'junk')]),
        ),
    ]
