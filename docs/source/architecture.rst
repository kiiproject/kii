Architecture
============

Here is a quick overview of kii architecture, so you can quickly understand what are kii built-in components and their role.

Kii functionalities are splitted accross several Python packages, called :term:`apps <app>`. They are indeed regular django apps.

Kii apps references
*******************

api
---

Provides base API views and logic.

.. note::

    This app is not written yet.

app
---

Provides app-related features, such as base model and view, a registry and a base class for kii apps, autoregistration of kii apps urls, and menu management.

base_models
-----------

Provides many model mixins, base templates, views and forms that are used accross all model-related kii apps (stream, particularly).

It's a core part of kii.

classify
--------

Implements stream items tagging.

.. note::

    The foundations are here, but this app is not fully written. User interface, form and filtering are still to be done.

discussion
----------

Implements comments, trackbacks, pingbacks and webmentions for stream items.

.. note::

    Only comment-related logic has been written for now.

glue
----

A glue app that sticks all kii apps together. Especially, this app provides a default settings file, some base templates, and most of the default theme static files.

hook
----

This app is in charge of providing hook-logic, so third-party apps can extend or override the default behaviour of kii apps.

permission
----------

Implements all permission-related stuff on models, views and forms.

stream
------

A big one, because it implements the core design concept of kii: stream and items. This app relies heavily on most of other core apps, and also provides needed forms, views, urls and templates.

tests
-----

This package is used as a repository for testing code and data. It also provides test urls and settings.

theme
-----

This app should implements theme related logic (like template loaders), but the "how" part is not really clear in my head at the moment.

user
----

User related-stuff, such as login, registration, forgotten-password, etc.

.. note::

    Except for the login part, almost averything needs to be done here.

utils
-----

A collection of utility classes and functions that does not fit in other apps.


