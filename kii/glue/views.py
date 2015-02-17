from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _

from kii.app.views import AppMixin
from kii.user import get_kii_users_group
from kii.stream.models import StreamItem


class Home(AppMixin, TemplateView):
    template_name = "glue/home.html"
    page_title = _("kii.welcome")

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)

        kii_users = get_kii_users_group().user_set.order_by('username')
        context['kii_users'] = kii_users
        context['last_items'] = StreamItem.objects.readable_by(self.request.user).exclude(importance=1)

        return context
