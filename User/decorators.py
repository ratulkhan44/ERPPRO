from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.core.exceptions import PermissionDenied

def required_role(allowed_roles=[]):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if str(request.user.user_role) in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('permission_denied')

        return wrap

    return decorator
        