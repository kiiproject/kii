from kii.discussion import models

import django.db.models

class DiscussionModel(models.DiscussionMixin):
    pass

class DiscussionModelComment(models.CommentMixin):
    subject = django.db.models.ForeignKey(DiscussionModel, related_name="comments")

    def set_publish(self):
        publish  = super(DiscussionModelComment, self).set_publish()

        if self.profile.email.startswith('publish'):
            publish = True

        return publish