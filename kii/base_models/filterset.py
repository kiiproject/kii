import django_filters

from . import models

class BaseFilterSet(django_filters.FilterSet):
    """A base class for more advanced FilterSets. 

    FilterSets are used to parse querystring from a URL and transpose it into a corresponding
    queryset. For example, a call on a List view with the URL ``/myapp/mymodel/list?status=draft``
    would be, under the hood, converted into ``MyModel.objects.filter(status="draft")``.

    Please report to `django_filters documentation`_ for in-depth explanation.

    .. _django_filters documentation: https://django-filter.readthedocs
    """


    class Meta:
        pass