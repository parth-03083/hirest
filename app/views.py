from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from .forms import * 
from django.template.loader import render_to_string
from django.http import JsonResponse , HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
# Create your views here.
from .models import *
import hirest.settings as settings
import http.client

def send_message(number,message):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)
    number = '+91' + str(number)

    message = client.messages.create(
                              body=message,
                              from_='+15075745390',
                              to=number)

    print(message.sid)




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

@login_required(login_url='login')
def applyView(request):
    if request.user.is_authenticated:
        try:
            user=MyProfile.objects.get(user=request.user)
            job_id=int(request.GET.get('job_id'))
            job=Job.objects.get(id=job_id)
            applied_job=AppliedJobs.objects.get_or_create(user=user,job=job)
            return redirect('jobs')
        except MyProfile.DoesNotExist:
            return redirect('add-profile')
    else:
        return redirect('login')
        
@login_required(login_url='login')
def myAppliedJobView(request):
    if request.user.is_authenticated:
        try:
            user=MyProfile.objects.get(user=request.user)
            applied_jobs=AppliedJobs.objects.filter(user=user)
            context={'jobs':applied_jobs}
            return render(request,'applied_jobs.html',context=context)
        
        except MyProfile.DoesNotExist:
            return redirect('add-profile')
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

@login_required(login_url='login')
def createProfileView(request):
    form = ProfileForm()
    skillform = SkillForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('index')
    return render(request, 'profile_form.html', {'form': form, 'header': False ,'skillform' : skillform})

def myProfileView(request):
    skillform = SkillForm()
    try:
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_authenticated and MyProfile(user=request.user):
                obj = MyProfile.objects.get(user=request.user)
                form = ProfileForm(instance=obj)
        else:
            form = ProfileForm()

        if request.method == 'POST':
            if request.user.is_authenticated and MyProfile(user=request.user):
                obj = MyProfile.objects.get(user=request.user)
                form = ProfileForm(request.POST , instance=obj)
            elif not request.user.is_authenticated:
                return redirect('login')
            else:
                form = ProfileForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')
    except MyProfile.DoesNotExist:
        return redirect('add-profile')
    
    return render(request, 'profile.html', {'form': form ,'skillform':skillform, 'header': False})

@login_required(login_url='login')
def postJobView(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if ishr(request.user):
        form = PostJobForm()
        try:
            profile=MyProfile.objects.get(user=request.user)
            if request.method == 'POST' and ishr(request.user):
                form = PostJobForm(request.POST)
                if form.is_valid():
                    object = form.save(commit=False)
                    skills = request.POST.getlist('skills')
                    skills = Skills.objects.filter(id__in=skills)
                    object.save()
                    for i in skills:
                        object.skills.add(i)
                    p = MyProfile.objects.get(user=request.user)
                    company_id = p.current_company
                    print("===profile_obj===",company_id)
                    object.company_name = p.current_company
                    object.save()
                    return redirect('index')
            return render(request, 'post_job.html', {'form': form,'profile':profile})
        except MyProfile.DoesNotExist or Company.DoesNotExist:
            if MyProfile.DoesNotExist:
                return redirect('add-profile')
            elif Company.DoesNotExist:
                return redirect('create-company')



@login_required(login_url='login')
def JobApplicationView(request):
    print(ishr(user=request.user))
    if request.user.is_authenticated and ishr(request.user) :
        try:
            user=request.user
            profile=MyProfile.objects.get(user=user)
            company=profile.current_company
            jobs=Job.objects.filter(company_name=company)
            context={'jobs':jobs}
            return render(request,'job_application.html',context=context)
        except MyProfile.DoesNotExist:
            return redirect('add-profile')
    elif not ishr(request.user):
        return redirect('create-company')
    else:
        return redirect('login')
    
@login_required(login_url='login')
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

@login_required(login_url='login')
def jobDeleteView(request,id):
    if ishr(request.user):
        job=Job.objects.get(id=id)
        job.delete()
        response = {
            'status' : 'success'
        }
        return JsonResponse(response)

@login_required(login_url='login')
def jobApplicantsView(request,id):
    if ishr(request.user):
        job=Job.objects.get(id=id)
        applicants=AppliedJobs.objects.filter(job=job)
        
        skills = list(set(job.skills.all()))
        
        # applicants = sorted(applicants, key=lambda x: sum([1 for i in x.user.skills.all() if i.name in skills ]), reverse=True)

        context={'applicants':applicants}

        return render(request,'job_applicants.html',context=context)

@login_required(login_url='login')
def viewUserProfileView(request,id):
    if ishr(request.user):
        user = User.objects.get(id=id)
        user_profile=MyProfile.objects.get(user=user)
        context={'user':user,'user_profile':user_profile}
        return render(request,'view_profile.html',context=context)
    else:
        return HttpResponse('You are not allowed to access this')
    

@login_required(login_url='login')
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

@login_required(login_url='login')
def updateCompanyProfile(request):
    form = CompanyForm()
    try:
        company = MyProfile.objects.get(user=request.user).current_company
        if not company:
            return redirect('create-company')
        form = CompanyForm(instance=company)
        if request.method == 'POST':
            form = CompanyForm(request.POST, instance=company)
            if form.is_valid():
                form.save()
            return redirect('index')
        return render(request, 'update_company_profile.html', {'form': form})
    except MyProfile.DoesNotExist:
        return redirect('my-profile')
    
    


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

    skills = MyProfile.objects.get(user=request.user).skills.all().values_list('name', flat=True)

    job = sorted(job, key = lambda x: sum([1 for i in x.skills.all() if i.name in skills]), reverse=True)

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
    
@login_required(login_url='/login')
def careerTestView(request):
    return render(request,'riasec_test.html')

@login_required(login_url='/login')
def careerInfoViewRIASEC(request):
    try:
        obj = UserRISECScore.objects.get(user=request.user)
        riasce = obj.marks
        careers = Careers.objects.none()
        for c in riasce:
            career = Careers.objects.filter(risec__icontains=c)
            careers = careers | career

        careers = sorted(careers,  key=lambda x: sum(1 for c in riasce if c in x.risec),reverse=True)

        print(careers)
        return render(request, 'careers.html', {'careers': careers})
    except:
        return redirect('riasec-test')
    


@login_required(login_url='/login')
def saveRISECcode(request):
    score = request.GET.get('score',False)
    user = request.user
    if UserRISECScore.objects.get(user=request.user).exists():
       obj =  UserRISECScore.objects.get(user=request.user)
       obj.marks=score
       obj.save()
    else:
        obj = UserRISECScore.objects.create(user=request.user,marks=score)
    response = {}
    response['status'] = 'success'
    response['message'] = 'Score added'

@login_required(login_url='login')
def createStartup(request):
    form = StartupForm()
    if request.method == 'POST':
        form = StartupForm(request.POST)
        obj = form.save(commit=False)
        if not StartUps.objects.get(created_by = request.user).exitst():
            obj.created_by = request.user
            obj.save()
            response ={}
            response['status'] = 'success'
            response['messafe'] = 'Startup Created Successfully'
            return JsonResponse(response)
        else:
            return HttpResponse('You can create only one startup')
    context = {'form':form}
    return render(request,'startup_form.html',context)


@login_required(login_url='login')
def updateStartup(request):
    try:
        instance = StartUps.objects.get(request=request.user)
        form = StartupForm(instance=instance)
        if request.method == 'POST':
            form = StartupForm(request.POST,instance=instance)
            if form.is_valid():
                form.save()
        context = {'form':form}
        return render(request,'startup_form.html',context)

    except StartUps.DoesNotExist:
        return redirect('create-startup')


@login_required(login_url='login')
def joinStartupView(request,id):
    try:
        user = request.user
        startup = StartUps.objects.get(id=id)
        obj = StartUpTeam.objects.create(user=request.user,startup=startup)
        context = {}
        context['status'] = 'success'
        context['message'] = 'Startup Created Successfully'
        return redirect('update-startup')

    except StartUps.DoesNotExist:
        return HttpResponse('following startup does not exist')
    

@login_required(login_url = 'login')
def appliedStartupView(request,id):
    try:
        startup = StartUps.objects.get(id=id)
        applicants = StartUpTeam.objects.filter(startup = startup)
        return render (request,'startup_applicants.html',{'applicants':applicants})
    except StartUpTeam.DoesNotExist or StartUps.DoesNotExist:
        if StartUps.DoesNotExist:
            return redirect('create-startup')
        if StartUpTeam.DoesNotExist:
            return HttpResponse('No applicants has applied')


@login_required(login_url='login')
def approveJoinStartup(request,id):    
    startup = StartUps.objects.get(created_by=request.user)
    applicant = User.objects.get(username=id)
    obj = StartUpTeam.objects.get(startup=startup,user=applicant)
    obj.is_approved = True
    context = {}
    context['status'] = 'successs'
    context['Message'] = 'Approved StartUp Team'

    return JsonResponse(context)

def jobDetailView(request,id):
    job = Job.objects.get(id=id)
    context = {'job':job}
    return render(request,'job_details.html',context)


@login_required(login_url='/login')
def sharityFunctionality(request):
    form = FileForm()
    if request.method == 'POST':
        form = FileForm(request.POST)
        print(form)
<<<<<<< HEAD
        try:
            if form.is_valid():
                print("form is valid")
                obj = form.save(commit = False)
                obj.user = request.user
                obj.save()
                print(obj.file)
                return HttpResponse('successs')
            else:
                print("form is not valid")
                return HttpResponse('failure')
        except Exception as e:
            print(f"Error submitting form: {e}")
            return HttpResponse('error')
=======
        if form.is_valid():
            print("form is valid")
            obj = form.save(commit = False)
            obj.user = request.user
            obj.save()
            print(obj.file)
            file = obj.file
            rows =  file.readlines()
            for i in rows:
                send_message()

            return HttpResponse('successs')
        else:
            print("form is not valid")
            return HttpResponse('failure')
>>>>>>> 7d8287744651521031a68086517fa4c06fbd4eea
    else:
        return render(request,'share-doc.html',{'form':form})


@login_required(login_url='/login')
def approveCandidate(request,id):
    try:
        obj = AppliedJobs.objects.get(id=id)
        obj.status = 'accepted'
        obj.save()
        message = 'Congratulations, you are selected in recent job you\'ve applied at ' + str(obj.job.company_name) + '.'
        number = obj.user.mobile_no
        send_message(number,message)
    

    except AppliedJobs.DoesNotExist or MyProfile.DoesNotExist :
        if AppliedJobs.DoesNotExist:
            return HttpResponse('apply to a job first')
        elif MyProfile.DoesNotExist:
            return redirect('my-profile')

@login_required(login_url='/login')
def interviewCandidate(request,id):
    try:
        obj = AppliedJobs.objects.get(id=id)
        obj.status = 'interview'
        obj.save()
        message = 'Congratulations, you are selected for interview in recent job you\'ve applied at ' + str(obj.job.company_name) + '.'
        number = obj.user.mobile_no
        send_message(number,message)

    except AppliedJobs.DoesNotExist or MyProfile.DoesNotExist :
        if AppliedJobs.DoesNotExist:
            return HttpResponse('apply to a job first')
        elif MyProfile.DoesNotExist:
            return redirect('my-profile')


@login_required(login_url='/login')
def rejectCandidate(request,id):
    try:
        obj = AppliedJobs.objects.get(id=id)
        obj.status = 'rejected'
        obj.save()
        message = ' You are Rejected from recent applied position at ' + str(obj.job.company_name) + '.'
        number = obj.user.mobile_no
        send_message(number,message)

    except AppliedJobs.DoesNotExist or MyProfile.DoesNotExist :
        if AppliedJobs.DoesNotExist:
            return HttpResponse('apply to a job first')
        elif MyProfile.DoesNotExist:
            return redirect('my-profile')

        
def exportResume(request):
    
    conn = http.client.HTTPSConnection("api.apyhub.com")
    instance = MyProfile.objects.get(user = request.user)
    form = ProfileForm(instance=instance)
    file = render(request,'profile.html',{'form':form})
    payload = "{\n    \"content\":\" <html> <body> <h1> Hello World </h1> </body> </html>"+ file +"\"\n}"

    headers = {
        'apy-token': "APY0Ih0X5wtdpdCZk5h8fGPU44JuROMgIkmPxCcIdFiQXfqa4mDP84W3dn7osnTpKBkE00vTi2",
        'Content-Type': "application/json"
        }

    conn.request("POST", "/generate/html-content/pdf-url?output=test-sample.pdf", payload, headers)

    res = conn.getresponse()
    data = res.read()
    
    return JsonResponse(data)

    



