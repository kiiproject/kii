import user
import stream


class StreamTestCase(user.tests.base.UserTestCase):

    def setUp(self):
        super(StreamTestCase, self).setUp()
        
        self.streams = {
            0: stream.models.Stream(owner=self.users[0], name="test0"),
        }
        for key, instance in self.streams.items():
            instance.save()