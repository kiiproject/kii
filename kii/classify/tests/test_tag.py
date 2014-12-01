import django.db
import django.core.exceptions
from django.core.urlresolvers import reverse

import kii.stream.tests.base
from kii import stream, classify
from kii.classify import models


class Tag(stream.tests.base.StreamTestCase):
    

    def test_can_add_stream_item_to_tag(self):
        s = self.streams[0]
        t = self.G(classify.models.Tag, name="yolo", owner=s.owner)

        si = self.G(stream.models.StreamItem, name="Hop la", stream=s)
        wsi = self.G(classify.models.TagStreamItem, tag=t, streamitem=si)

        self.assertEqual(classify.models.TagStreamItem.objects.all()[0], wsi)

    def test_can_query_tags_from_stream_item(self):

        s = self.streams[0]
        t = self.G(classify.models.Tag, name="yolo", owner=s.owner)

        si = self.G(stream.models.StreamItem, name="Hop la", stream=s)
        wsi = self.G(classify.models.TagStreamItem, tag=t, streamitem=si)

        self.assertEqual(si.tags.all()[0], t)

    def test_can_store_tag_hierarchically(self):
        s = self.streams[0]
        t0 = self.G(classify.models.Tag, name="level0")
        t1 = self.G(classify.models.Tag, name="level1", parent=t0)
        t2 = self.G(classify.models.Tag, name="level2", parent=t1)

    def test_tag_create(self):
        url = reverse('kii:classify:tag:create')
        self.login(self.users[0].username)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {"title": "Hello"})

        tag = models.Tag.objects.get(owner=self.users[0])
        self.assertEqual(tag.title, "Hello")