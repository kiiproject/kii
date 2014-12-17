from django.shortcuts import get_object_or_404

from kii.base_models import views
from . import forms

class CommentCreate(views.Create):
    
    form_class = forms.CommentForm

    def get_subject(self):
        # pass comment subject to form
        subject_model = self.form_class.Meta.model._meta.get_field('subject').rel.to
        self.subject = get_object_or_404(subject_model, pk=self.kwargs['pk'], discussion_open=True)
        return self.subject
        
    def get_form_kwargs(self, **kwargs):
        kwargs = super(CommentCreate, self).get_form_kwargs(**kwargs)
        kwargs['subject'] = self.get_subject()
        return kwargs

    def get_success_url(self):
        return self.get_subject().get_absolute_url()

class CommentFormMixin(object):
    """pass a comment form for the object to context"""

    form_class = forms.CommentForm
    
    def get_context_data(self, **kwargs):
        context = super(CommentFormMixin, self).get_context_data(**kwargs)

        context['comment_form'] = self.comment_form_class(request=self.request, user=self.request.user)
        return context