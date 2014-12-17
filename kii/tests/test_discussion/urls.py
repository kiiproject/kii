from django.conf.urls import patterns, url, include
from kii.discussion import views
from .. import views as test_views
from . import forms

dicussion_model_patterns = patterns('',
    url(r'^(?P<pk>\d+)/comments/add$', views.CommentCreate.as_view(form_class=forms.DiscussionModelCommentForm),
        name='comment_create'),
    url(r'^(?P<pk>\d+)$', test_views.blank, name="detail")
)

urlpatterns = patterns('',
     url(r'^$', test_views.blank, name='index'),
     url(r'^discussionmodel/', include(dicussion_model_patterns, namespace='discussionmodel')),
)
