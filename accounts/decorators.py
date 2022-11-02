from django.shortcuts import redirect, render
from .models import EmployeeDetails


def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            username = (request.user)
            if username.groups.filter(name='admin').exists():
                return redirect('home')
            elif username.groups.filter(name='hrteam').exists():
                return redirect('hr-home')
            else:
                ifid = EmployeeDetails.objects.get(empname=username).if_id
                return redirect('pnhome')
        else:
            return view_func(request,*args,**kwargs)

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return render(request,'errors/403.html')
        return wrapper_func
    return decorator