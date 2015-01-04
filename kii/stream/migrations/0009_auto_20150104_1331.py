# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth import get_user_model
from actstream.actions import follow
from actstream import registry


def subscribe_users(apps, schema_editor):
    """Subscribe legacy users to their stream activity. It is done
    automatically for newly created users"""

    stream_model = apps.get_model("stream", "Stream")
    registry.register(stream_model)
    for user in get_user_model().objects.all():
        stream = stream_model.objects.get(title=user.username, owner=user)        
        follow(user, stream, actor_only=False)


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0008_auto_20150101_2320'),
    ]

    operations = [
        migrations.RunPython(subscribe_users),
    ]
