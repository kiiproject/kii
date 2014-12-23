from django import template

register = template.Library()


@register.assignment_tag
def node_url(node, **kwargs):
    """

    Typical usage (look at ``kii/glue/templates/default/glue/menu_node.html`` for a real example):

    .. code-block:: html+django

        {% load app_tags %}

        {% with node=app.menu %}

            {% node_url node as url %}
            <a href="{{ url }}">My app root menu node</a>

            {% for child_node in node.children %}
            
                {% node_url child_node as child_url %}
                <a href="{{ child_url }}">A child node</a> 

            {% endfor %}
        {% endwith %}

    :param node: a :py:class:`kii.app.menu.MenuNode` instance
    :param kwargs: kwargs that will be passed to the :py:funct:`reverse` function
    :return: the target URL of the menu node
    """

    return node.url(**kwargs)
