# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0002_auto_20141216_1106'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='streamitem',
            options={'ordering': ['-publication_date'], 'permissions': (('read', 'permissions.view'), ('write', 'permissions.edit'), ('delete', 'permissions.delete'))},
        ),
    ]
