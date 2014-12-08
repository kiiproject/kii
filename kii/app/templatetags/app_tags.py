from django import template

register = template.Library()


@register.assignment_tag
def node_url(node, **kwargs):
    return node.url(**kwargs)
