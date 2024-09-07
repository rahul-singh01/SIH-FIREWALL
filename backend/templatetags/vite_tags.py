import json
from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()

@register.simple_tag
def vite_asset(filename):
    manifest_path = settings.STATIC_ROOT / 'manifest.json'
    try:
        with open(manifest_path, 'r') as manifest_file:
            manifest = json.load(manifest_file)
    except FileNotFoundError:
        return static(filename)
    
    try:
        return static(f"assets/{manifest[filename]['file']}")
    except KeyError:
        return static(filename)