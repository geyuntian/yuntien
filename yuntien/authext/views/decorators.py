from django.http import *
from django.contrib.auth.models import User
from yuntien.authext.models.auth import *

#generic authorization decorator
def authorize(view, func):
    def decorator(method):
        def new_method(request, *args, **kwds):
            if not func(request, *args, **kwds):
                return view(request, *args, **kwds)
            return method(request, *args, **kwds)            
        return new_method
    return decorator

def _default_view(request, *args, **kwds):
    raise Http404

def _get_user(request, *args, **kwds):
    return request.user.is_authenticated()

def _is_admin(request, *args, **kwds):
    return request.user.is_superuser

#user authorization decorator
def check_user(view=_default_view, func=_get_user):
    return authorize(view, func)

#admin authorization decorator
def check_admin(view=_default_view, func=_is_admin):
    return authorize(view, func)

def _find_by_id(cls, request, *args, **kwds):
    if kwds.has_key('id'):
        return cls.objects.get(pk=(int(kwds['id'])))

#authorization decorator
def check_authorization(cls, operation, view=_default_view, finder=_find_by_id):
    
    def _authorize_obj(request, *args, **kwds):
        obj = None
        if operation != OPERATION_ADD:
            obj = finder(cls, request, *args, **kwds)
                
        auth = cls.get_auth_class().get_auth(obj, get_current_user())
    
        if auth.has_key(operation):
            return auth[operation]
        else:
            return False
    
    return authorize(view, _authorize_obj)

#check id decorator
def _check_obj(cls, view=_default_view, finder=_find_by_id):
    def decorator(method):  
        def new_method(request, *args, **kwds):
            if not finder or not finder(cls, request, *args, **kwds):
                return view(request)
            
            return method(request, *args, **kwds)            
        return new_method
    return decorator

#check name decorator
def check_username(view=_default_view, name='user'):
    def _find(cls, request, *args, **kwds):
        if kwds.has_key(name):
            return User.objects.get(username=kwds[name])
    return _check_obj(User, view, finder=_find)
