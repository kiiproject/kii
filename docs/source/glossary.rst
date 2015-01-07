Glossary
========

.. glossary::

    instance
    
        A dedicated kii installation.

    app

        A python package that extends kii with a given set of features (e.g. a blog app). This term may also refer to kii's built-in apps, or to a regular django app. In fact, a kii app is also a django app.

    stream

        A feed that is owned by a user and contains an unlimited amount of items. If it helps you, you can picture a stream as a facebook wall: a place you own, where you publish different types of things like statuses, pictures or videos.

    steam item

        A record, stored in a stream (it may also be referred to as an item). All stream items share a common behaviour (they have a title, a content area that accepts markdown, a publication date, a permission system...). In kii's (and django's) terminology, this common behaviour is called a model, and the records are model instances. Stream items are not limited to this common behaviour though, and may be extended via the creation of child models. 

        For exemple, blog entries and code snippets are two different and possible child models of a stream item. A blog entry may have a slug, while a code snippet may have syntax-highlighting and a language attribute, but both need the common behaviour of the stream item model (publication date, permissions and so on).

    theme
        todo
