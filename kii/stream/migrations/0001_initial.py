# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kii.base_models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='base_models.namemixin.title')),
                ('content', kii.base_models.fields.MarkupField()),
                ('content_markup_type', models.CharField(default='markdown', max_length=30, choices=[(b'', b'--'), (b'markdown', b'markdown'), (b'none', b'none')])),
                ('_content_rendered', models.TextField(editable=False)),
                ('owner', models.ForeignKey(related_name='streams', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'permissions': (('read', 'permissions.view'), ('write', 'permissions.edit'), ('delete', 'permissions.delete')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StreamItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='base_models.namemixin.title')),
                ('content', kii.base_models.fields.MarkupField()),
                ('content_markup_type', models.CharField(default='markdown', max_length=30, choices=[(b'', b'--'), (b'markdown', b'markdown'), (b'none', b'none')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('_content_rendered', models.TextField(editable=False)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='dra', max_length=5, choices=[('dra', 'base_models.status_mixin.draft'), ('pub', 'base_models.status_mixin.published')])),
                ('publication_date', models.DateTimeField(default=None, null=True, editable=False, blank=True)),
                ('inherit_permissions', models.BooleanField(default=True)),
                ('discussion_open', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(related_name='streamitems', editable=False, to=settings.AUTH_USER_MODEL)),
                ('polymorphic_ctype', models.ForeignKey(related_name=b'polymorphic_stream.streamitem_set', editable=False, to='contenttypes.ContentType', null=True)),
                ('root', models.ForeignKey(related_name='children', to='stream.Stream')),
            ],
            options={
                'abstract': False,
                'permissions': (('read', 'permissions.view'), ('write', 'permissions.edit'), ('delete', 'permissions.delete')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StreamItemComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', kii.base_models.fields.MarkupField()),
                ('content_markup_type', models.CharField(default='markdown', max_length=30, choices=[(b'', b'--'), (b'markdown', b'markdown'), (b'none', b'none')])),
                ('_content_rendered', models.TextField(editable=False)),
                ('published', models.BooleanField(default=False)),
                ('junk', models.NullBooleanField(default=None)),
                ('subject', models.ForeignKey(related_name='comments', to='stream.StreamItem')),
                ('user', models.ForeignKey(related_name='streamitemcomments', default=None, blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('user_profile', models.ForeignKey(default=None, blank=True, to='discussion.AnonymousCommenterProfile', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='stream',
            unique_together=set([('owner', 'title')]),
        ),
    ]
