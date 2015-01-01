from django import template

register = template.Library()


@register.inclusion_tag('glue/icon.html')
def icon(name):
    """
    Shortcut to display an icon in templates. Usage:

    .. code-block:: html+django

        {% load glue_tags %}

        {% icon "my-icon" %}
    """

    return {'icon': name}
