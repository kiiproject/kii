from django import template

register = template.Library()


@register.simple_tag
def node_url(node, **kwargs):
    return node.url(**kwargs)
