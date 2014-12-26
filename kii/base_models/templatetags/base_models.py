from django import template


register = template.Library()

@register.filter(name="list_item_template")
def list_item_template(item):
    """Find the list_item template that should render a given
    :py:class:`kii.base_models.models.BaseMixin` instance"""
    
    template_names = item.__class__.get_template_names("list_item")
    for name in template_names:
        try:
            template.loader.get_template(name)
            return name
        except template.TemplateDoesNotExist:
            pass


@register.filter(name="is_owner")
def is_owner(item, user):
    return item.owned_by(user)