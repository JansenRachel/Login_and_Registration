from django.shortcuts import render, redirect
from django.contrib import messages
# from .models import *
from .models import User
import bcrypt

def index(request):
    return render(request, "login_reg.html")

def new_user(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create (firstname = request.POST['firstname'], lastname = request.POST['lastname'], email = request.POST['email'], password = pw_hashed)
        request.session['firstname'] = user.firstname
        request.session['id'] = user.id
        print(user)
        return redirect('/sucessful_login')

    
def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if not user:
        messages.error(request, "No record of that email, please register first")
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    if user:
        logged_user = user[0]
    if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
        request.session['user_id'] = logged_user.id
        request.session['firstname'] = logged_user.firstname
        return redirect('/sucessful_login')


def sucessful_login(request):
    return render(request, "sucessful_login.html")

def logout(request):
    request.session.flush()
    return redirect('/')

