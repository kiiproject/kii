from django import template

register = template.Library()

@register.filter(name="list_item_template")
def list_item_template(item):
    """Find the list_item template that should render a given BaseModelMixin instance"""
    template_names = item.__class__.get_template_names("list_item")
    return template_names[0]

