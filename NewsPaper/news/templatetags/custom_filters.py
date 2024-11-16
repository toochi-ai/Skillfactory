from django import template

register = template.Library()

censor_list = ['Noboa', 'Hague', 'thought', 'beats']


@register.filter()
def censor(value):
    for i in censor_list:
        value = value.replace(i[1:], '*' * len(i[1:]))
    return value