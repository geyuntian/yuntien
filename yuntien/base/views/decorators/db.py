from django.http import *

def _default_view(request):
    raise Http404

def _find_by_id(cls, request, *args, **kwds):
    if kwds.has_key('id'):
        return cls.objects.get(pk=kwds['id'])

#check id decorator
def check_obj(cls, view=_default_view, finder=_find_by_id):
    def decorator(method):  
        def new_method(request, *args, **kwds):
            if not finder or not finder(cls, request, *args, **kwds):
                return view(request)
            
            return method(request, *args, **kwds)            
        return new_method
    return decorator

#check id decorator
def check_id(cls, view=_default_view):
    return check_obj(cls, view)

#check name decorator
def check_name(cls, prefix='', view=_default_view, name='name'):
    def _find(cls, request, *args, **kwds):
        if kwds.has_key(name):
            return cls.objects.get(key_name=prefix+kwds[name])
    return check_obj(cls, view, finder=_find)

#check id or name decorator
def check_id_or_name(cls, prefix='', view=_default_view):
    def _find(cls, request, *args, **kwds):
        if kwds.has_key('id_or_name'):
            if kwds['id_or_name'][0] >= '0' and kwds['id_or_name'][0] <= '9':               
                return cls.objects.get(pk=kwds['id_or_name'])
            else:
                return cls.objects.get(key_name=prefix+kwds['id_or_name'])
    return check_obj(cls, view, finder=_find)
