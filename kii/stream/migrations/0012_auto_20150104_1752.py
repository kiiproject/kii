# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0011_auto_20150104_1751'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stream',
            unique_together=None,
        ),
    ]
