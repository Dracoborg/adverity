from django import template
from django.utils.safestring import mark_safe

from adverity.dashboard.data.base import data

register = template.Library()

@register.inclusion_tag('dashboard/graph.html')
def graph(datasources = None, campaigns = None):
    return {"chart": data.plot( datasources, campaigns )}

