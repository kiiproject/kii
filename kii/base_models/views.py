from django.views.generic import (DetailView, ListView, CreateView,
                                  DeleteView, UpdateView)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django_filters.views import FilterMixin

from kii.app.views import AppMixin
from . import forms


class RequireAuthenticationMixin(AppMixin):
    """Force user authentication before calling :py:meth:`dispatch`"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RequireAuthenticationMixin, self).dispatch(*args,
                                                                **kwargs)


class ModelTemplateMixin(AppMixin):
    """Implements some convenient logic for:

    - deducing the correct template to use, from :py:attr:`model` and
    :py:attr:`action`
    - building the page title
    """

    action = None
    """: a string representing an action performed by the view, like update,
    delete, detail, list...
    """

    def get_template_names(self):
        """
        :return: an iterable of possible template names, deduced from
        :py:attr:`action` and :py:attr:`model`
        """

        if self.template_name:
            # use given template name
            return self.template_name

        return self.model.get_template_names(self.action)

    def get_model(self):
        # todo : seems pointless
        return self.model

    def get_breadcrumbs(self):
        """Prepend action and model label to the page title"""
        breadcrumbs = super(ModelTemplateMixin, self).get_breadcrumbs()
        return breadcrumbs + (
            (self.get_model_title(), None),
            (self.get_action_title(), None)
        )

    def get_model_title(self):
        return self.get_model()._meta.verbose_name_plural

    def get_action_title(self):
        return ""

    def get_context_data(self, **kwargs):
        context = super(ModelTemplateMixin, self).get_context_data(**kwargs)
        context["model"] = self.model
        context["action"] = self.action
        return context


class ModelFormMixin(ModelTemplateMixin):

    """Implements some common modelform view logic"""

    form_template = "base_models/modelform.html"

    @classmethod
    def as_view(cls, *args, **kwargs):
        """Deduce model from form class if needed"""
        if getattr(cls, "model", None) is None and kwargs.get('model') is None:
            form_class = kwargs.get('form_class', getattr(cls, "form_class"))
            kwargs['model'] = form_class.Meta.model
        return super(ModelFormMixin, cls).as_view(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ModelFormMixin, self).get_context_data(**kwargs)
        context['form_template'] = self.form_template
        return context

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ModelFormMixin, self).get_form_kwargs(**kwargs)
        if self.form_class is not None and issubclass(self.form_class,
                                                      forms.BaseMixinForm):
            kwargs['user'] = self.request.user
            kwargs['request'] = self.request
        return kwargs


class SingleObjectMixin(object):
    def get_breadcrumbs(self):
        return super(SingleObjectMixin, self).get_breadcrumbs() + (
            (self.object.get_title(), None),
        )


class Create(ModelFormMixin, CreateView):
    """A generic view for creating a new instance of a model"""
    action = "create"

    def get_action_title(self):
        return _('model.create')


class Update(SingleObjectMixin, ModelFormMixin, UpdateView):
    """A generic view for updating an existing instance of a model"""
    action = "update"

    def get_action_title(self):
        return _('model.update')


class Delete(SingleObjectMixin, ModelTemplateMixin, DeleteView):
    """A generic view for deleting an existing instance of a model"""

    action = "delete"
    template_name = "base_models/basemixin/delete.html"

    def get_success_url(self):
        return reverse("kii:glue:home")

    def get_action_title(self):
        return _('model.delete')


class Detail(SingleObjectMixin, ModelTemplateMixin, DetailView):
    """A generic view for detailing an existing instance of a model"""

    action = "detail"

    def get_model(self):
        return self.object.__class__

    def get_context_object_name(self, obj):
        return "object"


class List(FilterMixin, ModelTemplateMixin, ListView):
    """A generic view for listing many instances of a model"""

    action = "list"

    filterset_class = None

    filterset = None
    """:the filterset will be built automatically by the view from
    :py:attr:`filterset_class`, and used for advanced queryset filtering
    via GET parameters"""

    def get_queryset(self):
        """Filter the queryset using GET parameters, if needed"""

        queryset = super(List, self).get_queryset()
        if self.filterset_class is not None:
            filterset_kwargs = self.get_filterset_kwargs()
            filterset_kwargs['queryset'] = queryset
            self.filterset = self.filterset_class(**filterset_kwargs)
            queryset = self.filterset.qs

        return queryset

    def get_filterset_kwargs(self):
        """:return: required arguments for building the filterset"""
        return {'data': self.request.GET or {}}

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        if self.filterset is not None:
            context['filterset'] = self.filterset
            context['show_filters'] = True
        return context


class OwnerMixin(AppMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.owner is None:
            login = reverse('kii:user:login') + "?next=" + request.path
            return redirect(login)
        return super(OwnerMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OwnerMixin, self).get_context_data(**kwargs)
        context['owner'] = self.request.owner
        return context


class PermissionMixin(AppMixin):
    """A mixin that implements permission checks on single object
    related views.

    No check will be performed if :py:attr:`required_permission` is set to
    ``None``
    """

    required_permission = None
    """: a string indicating what kind of permission is required for displaying
    the view.

    The actuel check will be done via :py:meth:`has_required_permission`.
    """

    def pre_dispatch(self, request, *args, **kwargs):
        r = super(PermissionMixin, self).pre_dispatch(request, *args, **kwargs)
        if (self.required_permission is not None and
                not self.has_required_permission(request, *args, **kwargs)):
            return self.permission_denied()

        return r

    def has_required_permission(self, request, *args, **kwargs):
        """:return: A boolean indicating if the request user can access
        the view
        """
        return False

    def permission_denied(self):
        """:return: a response for the case where user has not the required
        permission
        """
        raise Http404


class SingleObjectPermissionMixin(PermissionMixin):
    """Implements basic pluggable permission logic on single object views"""

    def pre_dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super(SingleObjectPermissionMixin,
                     self).pre_dispatch(request, *args, **kwargs)


class MultipleObjectPermissionMixin(PermissionMixin):

    pass


class RequireOwnerMixin(SingleObjectPermissionMixin):

    """Permission mixin that checks the requested object is owned by
    ``request.user`` before granting access
    """

    required_permission = "owner"

    def has_required_permission(self, request, *args, **kwargs):
        return self.object.owned_by(request.user)


class OwnerMixinDetail(RequireOwnerMixin, OwnerMixin, Detail):
    pass


class OwnerMixinList(OwnerMixin, List):
    pass


class OwnerMixinCreate(OwnerMixin, Create):
    """A create view that set the newly created instance ``owner`` attribute to
     ``request.user``
     """

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerMixinCreate, self).form_valid(form)


class OwnerMixinUpdate(OwnerMixin, RequireOwnerMixin, Update):
    pass


class OwnerMixinDelete(OwnerMixin, RequireOwnerMixin, Delete):

    pass
