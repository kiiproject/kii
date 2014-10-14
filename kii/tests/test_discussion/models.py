from kii.discussion import models

import django.db.models

class DiscussionModel(models.DiscussionMixin):
    pass

class DiscussionModelComment(models.CommentMixin):
    subject = django.db.models.ForeignKey(DiscussionModel, related_name="comments")


def spam_domain_is_unwanted(**kwargs):
    
    if kwargs.get('instance').profile.email.endswith('spam'):
        return True
    return False

models.comment_detect_unwanted.connect(spam_domain_is_unwanted)