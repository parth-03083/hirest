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
        next_url = '/index'
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


def logout_view(request):
    logout(request)
    return redirect('login')

def jobView(request):
    jobs = Job.objects.all()
    context = {'jobs': jobs}
    return render(request, 'jobs.html', context=context)

def applyView(request):
    if request.user.is_authenticated:
        user=request.user
        job_id=int(request.GET.get('job_id'))
        job=Job.objects.get(id=job_id)
        applied_job=AppliedJobs.objects.get_or_create(user=user,job=job)
        return redirect('jobs')
    else:
        return redirect('login')
        
def myAppliedJobView(request):
    if request.user.is_authenticated:
        user=request.user
        applied_jobs=AppliedJobs.objects.filter(user=user)
        context={'jobs':applied_jobs}
        return render(request,'applied_jobs.html',context=context)
    else:
        return redirect('login')
    
def internShipView(request):
    internships=Internships.objects.all()
    context={'internships':internships}
    return render(request,'internships.html',context=context)

def startupView(request):
    startups=StartUps.objects.all()
    context={'startups':startups}
    return render(request,'startups.html',context=context)

def myProfileView(request):
    form = ProfileForm()
    form1 = NewUserForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'profile.html', {'form': form , 'form1':form1 , 'header': False})