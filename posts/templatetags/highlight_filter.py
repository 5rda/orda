from django import template

register = template.Library()

@register.filter
def highlight(value, query):
    return value.replace(query, f'<span class="highlight">{query}</span>')