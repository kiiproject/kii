import user.tests.base
import stream


class StreamTestCase(user.tests.base.UserTestCase):

    def setUp(self):
        super(StreamTestCase, self).setUp()
        
        self.streams = {
            0: stream.models.Stream(owner=self.users[0], name="test0"),
            1: stream.models.Stream(owner=self.users[1], name="test1"),
        }
        for key, instance in self.streams.items():
            instance.save()