from django import template
from django.urls.base import translate_url as trans_url

register = template.Library()


@register.simple_tag(takes_context=True)
def translate_url(context, lang):
    path = context["request"].get_full_path()
    return trans_url(path, lang)
