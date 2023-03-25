from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django import forms
from django.urls import reverse
from .forms import *
import datetime 
from django.template.loader import render_to_string
from django.http import JsonResponse , HttpResponse
from django.contrib.auth.models import Group
# Create your views here.
from .models import *


def is_ajax(request):
  return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def ishr(user):
    return user.groups.filter(name='hr').exists()

def indexView(request):
    jobs= Job.objects.all()
    is_hr = ishr(request.user)
    context={'jobs':jobs , 'is_hr':is_hr}
    
    return render(request,'home.html',context=context)

def loginView(request):
    header = False
    form = AuthenticationForm()
    if request.method == 'POST':
        next_url = '/'
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
                    return redirect('index')
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
        return redirect('add-profile')
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
        user=MyProfile.objects.get(user=request.user)
        job_id=int(request.GET.get('job_id'))
        job=Job.objects.get(id=job_id)
        applied_job=AppliedJobs.objects.get_or_create(user=user,job=job)
        return redirect('jobs')
    else:
        return redirect('login')
        
def myAppliedJobView(request):
    if request.user.is_authenticated:
        user=MyProfile.objects.get(user=request.user)
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

def createProfileView(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'profile_form.html', {'form': form, 'header': False})

def myProfileView(request):
    skillform = SkillForm()
    if request.user.is_authenticated and MyProfile(user=request.user):
            obj = MyProfile.objects.get(user=request.user)
            form = ProfileForm(instance=obj)
    else:
        form = ProfileForm()

    if request.method == 'POST':
        if request.user.is_authenticated and MyProfile(user=request.user):
            obj = MyProfile.objects.get(user=request.user)
            form = ProfileForm(request.POST , instance=obj)
        else:
            form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'profile.html', {'form': form ,'skillform':skillform, 'header': False})

def postJobView(request):
    if ishr(request.user):
        form = PostJobForm()
        profile=MyProfile.objects.get(user=request.user)
        if request.method == 'POST' and ishr(request.user):
            form = PostJobForm(request.POST)
            if form.is_valid():
                object = form.save(commit=False)
                object.company_name = MyProfile(user=request.user).current_company
                object.save()
                return redirect('index')
        return render(request, 'post_job.html', {'form': form,'profile':profile})

def JobApplicationView(request):
    print(ishr(user=request.user))
    if request.user.is_authenticated and ishr(request.user) :
        user=request.user
        profile=MyProfile.objects.get(user=user)
        company=profile.current_company
        jobs=Job.objects.filter(company_name=company)
        context={'jobs':jobs}
        return render(request,'job_application.html',context=context)
    else:
        return redirect('login')
    
def jobUpdateView(request,id):
    if ishr(request.user):
        job=Job.objects.get(id=id)
        form=PostJobForm(instance=job)
        if request.method == 'POST':
            form  = PostJobForm(request.POST,instance=job)
            if form.is_valid():
                form.save()
            return redirect('index')
        return render(request,'update_job.html',{'form':form})

def jobDeleteView(request,id):
    if ishr(request.user):
        job=Job.objects.get(id=id)
        job.delete()
        return redirect('index')


def jobApplicantsView(request,id):
    if ishr(request.user):
        job=Job.objects.get(id=id)
        applicants=AppliedJobs.objects.filter(job=job)
        context={'applicants':applicants}

        return render(request,'job_applicants.html',context=context)

def viewUserProfileView(request,id):
    user = User.objects.get(id=id)
    user_profile=MyProfile.objects.get(user=user)
    context={'user':user,'user_profile':user_profile}
    return render(request,'view_profile.html',context=context)

def createCompanyProfile(request):
    form = CompanyForm()
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            obj = form.save()
            profile = MyProfile.objects.get(user=request.user)
            profile.current_company = obj
            my_group = Group.objects.get(name='hr') 
            my_group.user_set.add(request.user)
            profile.save()
            return redirect('index')
    return render(request, 'create_company_profile.html', {'form': form})

def updateCompanyProfile(request):
    form = CompanyForm()
    company = MyProfile.objects.get(user=request.user).current_company
    form = CompanyForm(instance=company)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
        return redirect('index')
    return render(request, 'update_company_profile.html', {'form': form})

def searchJobs(request):
    title = request.GET.get('title',False)
    location = request.GET.getlist('location',False)
    experience = request.GET.get('experience',False)
    skills = request.GET.getlist('skills',False)
    companies = request.GET.getlist('company',False)

    job = Job.objects.all()
    startup = StartUps.objects.all()
    internship = Internships.objects.all()

    if title and len(title) > 0:
        job = job.filter(title__icontains=title)
        startup = startup.filter(name__icontains=title)
        internship = internship.filter(title__icontains=title)
    
    if location and len(location) > 0:
        job = job.filter(location__in=location)
        startup = startup.filter(location__in=location)
        internship = internship.filter(location__in=location)
    
    if experience and len(experience) > 0:
        job = job.filter(experience__icontains=experience)
        internship = internship.filter(experience__icontains=experience)

    if companies and len(companies) > 0:
        job = job.filter(company_name__name__in=companies)
        startup = startup.filter(name__in=companies)
        internship = internship.filter(company_name__name__in=companies)
    
    if skills and len(skills) > 0:
        job = job.filter(skills__name__in=skills)
        internship = internship.filter(skills__name__in=skills)


    if not is_ajax(request):
        location = list(set(Job.objects.values_list('location', flat=True)))
        skills = list(set(Skills.objects.values_list('name', flat=True)))
        companies = list(set(Job.objects.values_list('company_name__name', flat=True))).append(list(set(StartUps.objects.values_list('name', flat=True))))

        context = {'location': location , 'skills':skills , 'companies':companies}
        return render(request, 'jobs_search.html', context=context)
    

    content = render_to_string('jobs_object.html', {'jobs': job,'internship':internship,'startup':startup})

    return JsonResponse({'content': content}) 


def addSkillView(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        response={}
        response['status']=False
        if form.is_valid():
            form.save()
            response['status']=True
            return JsonResponse(response)
    else:
        return HttpResponse('Not Allowed')