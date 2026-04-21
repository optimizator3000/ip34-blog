from django.shortcuts import redirect, render
from .models import User

def login_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('/login')
        return func(request, *args, **kwargs)
    return wrapper