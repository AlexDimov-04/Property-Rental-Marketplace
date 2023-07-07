from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user_restricted(func_param):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return func_param(request, args, kwargs)
    
    return wrapper

def allowed_users(allowed_roles=[]):
    def decorator(func_param):
        def wrapper(request, *args, **kwargs):
            return func_param(request, *args, **kwargs)
        return wrapper
    return decorator
             