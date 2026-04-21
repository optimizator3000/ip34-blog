from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .forms import UserForm


def index(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    username = request.session.get('login')
    return render(request, "base.html", {'username': username})


def users(request):
    users = User.objects.all()
    return render(request, "users.html", {'users': users})


def add_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users/')
    else:
        form = UserForm()

    return render(request, "add_user.html", {'form': form})


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(login=username).first()

        if not user:
            messages.error(request, 'Пользователь не найден')
            return redirect('/login/')

        if password != user.password:
            messages.error(request, 'Неверный пароль')
            return redirect('/login/')

        request.session['user_id'] = user.id
        request.session['login'] = user.login

        return redirect('/')

    return render(request, 'login.html')


def logout(request):
    request.session.flush()
    messages.info(request, 'Вы вышли из системы')
    return redirect('/login/')


def edit_user(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/users/')
    else:
        form = UserForm(instance=user)

    return render(request, 'add_user.html', {'form': form})


def delete_user(request, user_id):
    user = User.objects.get(id=user_id)

    user.delete()
    return redirect('/users/')