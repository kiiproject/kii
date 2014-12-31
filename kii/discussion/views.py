from django.shortcuts import get_object_or_404
from django.contrib import messages

from kii.base_models import views
from . import forms


class CommentCreate(views.Create):
    """View for posting comments, the URL should include a ``pk`` argument,
    so checking on ``discussion_open`` can be run on the comment subject."""

    form_class = forms.CommentForm

    def get_subject(self):
        # deduce the subject model class from the form model
        subject_model = self.form_class.Meta.model._meta.get_field('subject').rel.to
        self.subject = get_object_or_404(subject_model, pk=self.kwargs['pk'],
                                         discussion_open=True)
        return self.subject

    def get_form_kwargs(self, **kwargs):
        kwargs = super(CommentCreate, self).get_form_kwargs(**kwargs)
        kwargs['subject'] = self.get_subject()
        return kwargs

    def get_success_url(self):
        """Redirect the user to the subject absolute URL"""
        return self.get_subject().get_absolute_url()

    def form_valid(self, *args, **kwargs):
        r = super(CommentCreate, self).form_valid(*args, **kwargs)
        if self.object.status == "published":
            message = "comment.publish.success"
        else:
            message = "comment.publish.success.awaiting_moderation"
        messages.success(self.request, message)
        return r


class CommentFormMixin(object):
    """pass a comment form for the object to context"""

    comment_form_class = forms.CommentForm

    def get_context_data(self, **kwargs):
        context = super(CommentFormMixin, self).get_context_data(**kwargs)

        context['comment_form'] = self.comment_form_class(
            request=self.request,
            user=self.request.user)

        return context
