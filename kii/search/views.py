from django import shortcuts
from django.db.models import Q

from kii.stream.models import Stream, StreamItem, ItemComment


def NavigationAutocomplete(request,
    template_name='search/autocomplete/navigation.html'):

    max_items = 5
    q = request.GET.get('q', '')

    queries = {}

    queries['streams'] = Stream.objects.filter(
        Q(title__icontains=q) |
        Q(content__icontains=q)
    ).readable_by(request.user).distinct()[:max_items]

    queries['items'] = StreamItem.objects.filter(
        Q(title__icontains=q) |
        Q(content__icontains=q)
    ).readable_by(request.user).distinct()[:max_items]

    return shortcuts.render(request, template_name, queries)