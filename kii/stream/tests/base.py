from ...user.tests import base
from .. import models


class StreamTestCase(base.UserTestCase):

    def setUp(self):
        super(StreamTestCase, self).setUp()
        
        self.streams = {
            0: models.Stream(owner=self.users[0], title="test0"),
            1: models.Stream(owner=self.users[1], title="test1"),
        }
        for key, instance in self.streams.items():
            instance.save()