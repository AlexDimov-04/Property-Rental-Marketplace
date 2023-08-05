from django.http import HttpResponse
from django.shortcuts import redirect


def allowed_users(allowed_roles=[]):
    def decorator(func_param):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return func_param(request, *args, **kwargs)          
            return HttpResponse('Not admin!')
        
        return wrapper
    
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'renter':
            return redirect('index')
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        
    return wrapper_function
