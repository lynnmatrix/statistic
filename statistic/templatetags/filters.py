from django import template

register = template.Library()


@register.filter
def get_dict(h, name):
	return h[name]
