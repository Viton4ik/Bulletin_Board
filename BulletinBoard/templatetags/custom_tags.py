
from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """ 
    if using pangination+filter -> not to cancel filter if click to the next page 
    - url corrected needed
    - example:
        before: 
            href="?page={{ page_obj.previous_page_number }}"
        after:
            href="?{% url_replace page=page_obj.previous_page_number %}"
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
    