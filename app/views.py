from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django import forms
from django.urls import reverse
from .forms import *
# Create your views here.
from .models import *

def indexView(request):
    jobs= Job.objects.all()
    context={'jobs':jobs}
    # print(jobs[0])
    return render(request,'home.html',context=context)

def loginView(request):
    header = False
    form = AuthenticationForm()
    if request.method == 'POST':
        next_url = request.POST['next']
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                print(next_url)
                if 'login' not in next_url.split('/'):
                    return redirect(next_url)
                else:
                    return redirect(reverse('index'))
        else:
            messages.error(request, 'username or password not correct')
    return render(request, 'login.html', {'form': form, 'header': False})


def signup(request):
    header = False
    form = NewUserForm()
    profile_form = NewUserForm()
    if request.method == 'POST':

        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
        login(request, user)
        return redirect(reverse('login'))

    return render(request, 'register.html', {'form': form, 'header': False})