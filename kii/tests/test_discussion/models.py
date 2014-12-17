import django.db.models
from django.core.urlresolvers import reverse

from kii.discussion import models


class DiscussionModel(models.DiscussionMixin):
    pass
    def reverse_comment_create(self, **kwargs):
        """Return URL for posting a comment"""
        return reverse("kii:test_discussion:discussionmodel:comment_create", kwargs={"pk": self.pk})

class DiscussionModelComment(models.CommentMixin):
    subject = django.db.models.ForeignKey(DiscussionModel, related_name="comments")



def spam_domain_is_junk(**kwargs):
    
    if kwargs.get('instance').profile.email.endswith('spam'):
        return True
    return False

models.comment_detect_junk.connect(spam_domain_is_junk)