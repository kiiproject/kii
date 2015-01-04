# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from actstream.actions import follow


def subscribe_users(apps, schema_editor):
    """Subscribe legacy users to their stream activity. It is done
    automatically for newly created users"""

    for user in apps.get_model("auth", "User").objects.all():
        stream = user.streams.filter(title=user.username)
        follow(user, stream, actor_only=False)


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0008_auto_20150101_2320'),
    ]

    operations = [
        migrations.RunPython(subscribe_users),
    ]
