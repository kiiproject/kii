Under the hood
==============

You'll find here some technical informations about kii.

Server-side
###########

Programming language
********************

Kii is written in Python_, and should work under both Python 2 and 3. The test suite is run under Python 2.7 and 3.4. While Python's standard library is used in many place, kii requires some additional packages:

- Markdown_, for well... Markdown syntax formatting
- Six_, for Python 2 and 3 compatibility

.. _Python: http://www.python.org/
.. _Markdown: https://github.com/waylan/Python-Markdown
.. _Six: http://pythonhosted.org/six/

Framework
*********

Kii runs on top of Django_, the web framework for perfectionnists with deadlines. This choice has been made because, by nature, Django is very extensible, and many great django apps are useful in the scope ofo the project, such as:

- Polymorphic_, used for convenient inheritance of stream items behaviour, at a database level
- Guardian_, for per-object permissions
- MPTT_, for tags hierarchy
- `REST framework`_, for the REST API
- Filter_, for complex filtering of stream items via URL parameters

.. _Django: https://www.djangoproject.com/
.. _Polymorphic: https://github.com/chrisglass/django_polymorphic
.. _Guardian: https://github.com/lukaszb/django-guardian/
.. _MPTT: https://github.com/django-mptt/django-mptt/
.. _REST framework: http://www.django-rest-framework.org/
.. _Filter: https://github.com/alex/django-filter

Testing
*******

Testing is done via Nose_ and Tox_.

.. _Nose: http://nose.readthedocs.org/en/latest/
.. _Tox: http://tox.readthedocs.org

Client-side
###########

- Foundation_ and `Foundation icon fonts`_, for the default theme
- AngularJS_, for comments administration interface
  
.. _Foundation: http://foundation.zurb.com/
.. _Foundation icon fonts: http://zurb.com/playground/foundation-icon-fonts-3
.. _AngularJS: https://angularjs.org/
