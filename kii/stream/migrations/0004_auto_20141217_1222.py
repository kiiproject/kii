# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kii.base_models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discussion', '0001_initial'),
        ('stream', '0003_auto_20141216_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', kii.base_models.fields.MarkdownField()),
                ('content_markup_type', models.CharField(default='markdown', max_length=255)),
                ('_content_rendered', models.TextField(default='')),
                ('published', models.BooleanField(default=False)),
                ('junk', models.NullBooleanField(default=None)),
                ('subject', models.ForeignKey(related_name='comments', to='stream.StreamItem')),
                ('user', models.ForeignKey(related_name='itemcomments', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_profile', models.ForeignKey(default=None, blank=True, to='discussion.AnonymousCommenterProfile', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='streamitemcomment',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='streamitemcomment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='streamitemcomment',
            name='user_profile',
        ),
        migrations.DeleteModel(
            name='StreamItemComment',
        ),
    ]
