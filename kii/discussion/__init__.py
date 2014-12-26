"""
Example of implementation
*************************

Here is a quick example of discussion integration on your own models.

Models
------

.. code-block:: python
        
    # myapp/models.py

    from django.db import models
    from kii.discussion.model import CommentMixin, DiscussionMixin


    class BlogEntry(DiscussionMixin):
        title = models.CharField(max_length=255)
        content = models.TextField()


    class BlogEntryComment(CommentMixin):
        subject = models.ForeignKey(BlogEntry)

After a ``python manage.py syncdb``, you should be able to run the following in a shell:

.. code-block:: python

    >>> from myapp import models
    >>> from django.contrib.auth import get_user_model
    >>> blog_entry = models.BlogEntry(title="Hello world", content="Yolo!", discussion_open=True)
    >>> blog_entry.save()
    >>> comment_user = get_user_model().objects.get(username="jeanmichel)
    >>> comment = models.BlogEntryComment(user=comment_user, subject=blog_entry, content="Nice post dude!")
    >>> comment.save()
    >>> assert blog_entry.comments.all().first() == comment

Form
----

.. code-block:: python

    # myapp/forms.py

    from kii.discussion.forms import CommentForm
    from . import models


    class BlogEntryCommentForm(CommentForm):
        class Meta(CommentForm.Meta):
            model = models.BlogEntryComment

View
----

.. code-block:: python

    # myapp/views.py

    from django.views.generic import DetailView
    from kii.discussion import views

    from . import models, forms

    class BlogEntryDetail(views.CommentFormMixin, DetailView):

        model =  models.BlogEntry
        comment_form_class = forms.BlogEntryCommentForm


URLs
----

.. code-block:: python

    # myapp/urls.py

    from django.conf.urls import patterns, url
    from . import views, forms
    from kii.discussion.views import CommentCreate


    urlpatterns = patterns('',
        url(r'^(?P<pk>\d+)$', views.BlogEntryDetail.as_view(), name='entry_detail'),
        url(r'^(?P<pk>\d+)/comments/add$', CommentCreate.as_view(
            form_class=forms.BlogEntryCommentForm), name='comment_create'),
    )

Template
--------

.. code-block:: html+django

    # myapp/templates/myapp/blog_entry_detail.html

    <h1>{{ object.title }}</h1>
    {{ object.content }}

    {% if object.discussion_open %}
        <ul class="comments">
            {% for comment in object.comments.public %}
                <li>
                    <h2>{{ comment.profile.username }}</h2>
                    <p>{{ comment.created|timesince }} ago</p>
                    {{ comment.content }}
                </li>
            {% endfor %}
        </ul>
        <h1>Publish a comment</h1>
        <form action="{% url 'comment_create' pk=object.pk %}" method="POST">
            {% csrf_token %}
            {{ comment_form.as_p }}
            <input type="submit" value="OK" />
        </form>
    {% else %}
        Discussion is closed for this entry.
    {% endif %}
"""