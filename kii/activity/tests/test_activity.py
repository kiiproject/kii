from kii.stream.tests import base
from kii.stream import models as stream_models


class NotificationTestCase(base.StreamTestCase):

    def test_notification_is_created_for_each_following_user(self):

        stream = stream_models.Stream.objects.get_user_stream(self.users[0])

        si = self.G(stream_models.StreamItem, root=stream)
        c = self.G(stream_models.ItemComment, subject=si, user=self.users[1])

        self.assertEqual(self.users[0].notifications.all().first().action.action_object,
                         c)



