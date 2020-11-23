from django import template

register = template.Library()

def make_string(value):
    return str(value)

register.filter('make_string',make_string)