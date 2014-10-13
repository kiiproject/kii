from kii.discussion import models

import django.db.models

class DiscussionModel(models.DiscussionMixin):
    pass

class DiscussionModelComment(models.CommentMixin):
    subject = django.db.models.ForeignKey(DiscussionModel, related_name="comments")