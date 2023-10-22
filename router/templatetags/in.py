from django import template

register = template.Library()


@register.filter
def isin(value, arg):
    return value in arg


@register.filter
def get(value, arg):
    return value.get(arg)


@register.filter
def checked(value, filter):
    return value, filter


@register.filter
def request(a, req):
    value, filter = a

    if str(filter) not in req.POST:
        return False
    return str(value["id"]) in req.POST.getlist(str(filter))


@register.filter
def orfrommin(a, req):
    value, filter = a
    if str(filter) not in req.POST:
        return value
    return req.POST.getlist(str(filter))[0]


@register.filter
def orfrommax(a, req):
    value, filter = a
    if str(filter) not in req.POST:
        return value
    return req.POST.getlist(str(filter))[1]
