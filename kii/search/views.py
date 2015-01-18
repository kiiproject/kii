from django import shortcuts
from django.db.models import Q

from kii.stream.models import Stream, StreamItem


def NavigationAutocomplete(request,
    template_name='search/autocomplete/navigation.html'):

    q = request.GET.get('q', '')

    queries = {}

    queries['streams'] = Stream.objects.filter(
        Q(title__icontains=q) |
        Q(content__icontains=q)
    ).readable_by(request.user).distinct()[:6]

    queries['items'] = StreamItem.objects.filter(
        Q(title__icontains=q) |
        Q(content__icontains=q)
    ).readable_by(request.user).distinct()[:6]

    return shortcuts.render(request, template_name, queries)