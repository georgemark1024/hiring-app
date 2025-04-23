from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='has_both_groups')
def has_both_groups(user):
    return (user.groups.filter(name="ServiceProvider").exists() and
            user.groups.filter(name="Client").exists())