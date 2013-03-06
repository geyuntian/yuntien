from django.http import *

def get_int_param(request, name, default):
    value = request.GET.get(name, default)
    try:
        return int(value)
    except:
        return default
    
def check_request_method(methods):
    def decorator(method):  
        def new_method(request, *args, **kwds):
            if request.method not in methods:
                raise Http404
            
            return method(request, *args, **kwds)            
        return new_method
    return decorator
