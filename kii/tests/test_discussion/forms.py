from kii.discussion import forms
from . import models

class DiscussionModelCommentForm(forms.CommentForm):

    class Meta(forms.CommentForm.Meta):
        model = models.DiscussionModelComment