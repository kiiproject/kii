import kii.stream.tests.base
from kii import stream, classify
import django.db
import django.core.exceptions


class TestWorkspace(stream.tests.base.StreamTestCase):
    
    def test_workspace_requires_stream(self):
        w = classify.models.Workspace(name="yolo")

        with self.assertRaises(django.db.IntegrityError):
            w.save()

    def test_can_add_stream_item_to_workspace(self):
        s = self.streams[0]
        w = classify.models.Workspace(name="yolo", stream=s)
        w.save()

        si = stream.models.StreamItem(name="Hop la", stream=s)
        si.save()
        wsi = classify.models.WorkspaceStreamItem(
                workspace=w, item=si)
        wsi.save()

    def test_cannot_save_streamitem_in_workspace_from_other_stream(self):
        s0 = self.streams[0]
        s1 = self.streams[1]
        w0 = classify.models.Workspace(name="s0", stream=s0)
        w1 = classify.models.Workspace(name="s1", stream=s1)
        w0.save()
        w1.save()

        si = stream.models.StreamItem(name="Hop la", stream=s0)
        si.save()
        with self.assertRaises(django.core.exceptions.ValidationError):
            wsi = classify.models.WorkspaceStreamItem(
                workspace=w1, item=si)
            wsi.save()

    def test_can_store_workspace_hierarchically(self):
        s = self.streams[0]
        w0 = classify.models.Workspace(name="level0", stream=s)
        w0.save()
        w1 = classify.models.Workspace(name="level1", stream=s, parent=w0)
        w1.save()
        w2 = classify.models.Workspace(name="level2", stream=s, parent=w1)
        w2.save()
