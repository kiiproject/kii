import kii.stream.tests.base
from kii import stream, classify
import django.db
import django.core.exceptions
from django_dynamic_fixture import G

class Tag(stream.tests.base.StreamTestCase):
    
    def test_tag_requires_stream(self):
        w = classify.models.Tag(name="yolo")

        with self.assertRaises(AttributeError):
            w.save()

    def test_can_add_stream_item_to_tag(self):
        s = self.streams[0]
        w = classify.models.Tag(name="yolo", stream=s)
        w.save()

        si = stream.models.StreamItem(name="Hop la", stream=s)
        si.save()
        wsi = classify.models.TagItem(
                tag=w, item=si)
        wsi.save()

    def test_tag_inherit_owner_from_stream(self):
        w = G(classify.models.Tag, stream=self.streams[0])
        self.assertEqual(w.owner, w.stream.owner)

    def test_cannot_save_streamitem_in_tag_from_other_stream(self):
        s0 = self.streams[0]
        s1 = self.streams[1]
        w0 = classify.models.Tag(name="s0", stream=s0)
        w1 = classify.models.Tag(name="s1", stream=s1)
        w0.save()
        w1.save()

        si = stream.models.StreamItem(name="Hop la", stream=s0)
        si.save()
        with self.assertRaises(django.core.exceptions.ValidationError):
            wsi = classify.models.TagItem(
                tag=w1, item=si)
            wsi.save()

    def test_can_store_tag_hierarchically(self):
        s = self.streams[0]
        w0 = classify.models.Tag(name="level0", stream=s)
        w0.save()
        w1 = classify.models.Tag(name="level1", stream=s, parent=w0)
        w1.save()
        w2 = classify.models.Tag(name="level2", stream=s, parent=w1)
        w2.save()
