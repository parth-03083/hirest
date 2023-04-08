from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Skills(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company/',blank=True, null=True)
    website = models.CharField(max_length=100,blank=True, null=True)
    Employee = models.IntegerField(blank=True, null=True)
    founded_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    


class MyProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=13,blank=True, null=True)
    skills = models.ManyToManyField(Skills,blank=True)
    current_job=models.CharField(max_length=100,blank=True,null=True)
    current_company = models.ForeignKey(Company,on_delete=models.CASCADE,blank=True,null=True)
    education = models.TextField(blank=True,null=True)
    total_experience = models.CharField(max_length=10,blank=True,null=True)
    experties = models.IntegerChoices('experties', 'Beginner Intermediate Expert')

    def __str__(self):
        return self.user.username


class Job(models.Model):
    title=models.CharField(max_length=500,blank=True, null=True)
    company_name=models.ForeignKey(Company,on_delete=models.CASCADE , null=True)
    category = models.CharField(max_length=100,blank=True,null=True) 
    skills=models.ManyToManyField(Skills,blank=True,null=True)
    salary=models.BigIntegerField(blank=True, null=True)
    rank=models.IntegerField(blank=True,null=True)
    description=models.TextField(blank=True, null=True)
    experience=models.CharField(max_length=500,blank=True, null=True)
    location=models.CharField(max_length=500,blank=True, null=True)
    posted_date=models.DateTimeField(auto_now_add=True)
    last_date=models.DateTimeField(blank=True, null=True)


    class Meta:
        ordering = ['rank']

    def __str__(self):
        return self.title 

class AppliedJobs(models.Model):
    job=models.ForeignKey(Job,on_delete=models.CASCADE)
    user=models.ForeignKey(MyProfile,on_delete=models.CASCADE)
    applied_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job.title + '-' + self.user.user.username

class StartUps(models.Model):
    name=models.CharField(max_length=500,blank=True, null=True)
    description=models.TextField(blank=True, null=True)
    location=models.CharField(max_length=500,blank=True, null=True)
    logo=models.ImageField(upload_to='startup/',blank=True, null=True)
    website=models.CharField(max_length=500,blank=True, null=True)
    email=models.EmailField(blank=True, null=True)
    phone=models.CharField(max_length=500,blank=True, null=True)
    founded_date=models.DateTimeField(blank=True, null=True)
    created_by = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Internships(models.Model):
    title=models.CharField(max_length=500,blank=True, null=True)
    company_name=models.ForeignKey(Company,on_delete=models.CASCADE)
    skills=models.ManyToManyField(Skills,blank=True,verbose_name='Skills')
    salary=models.BigIntegerField(blank=True, null=True)
    rank=models.IntegerField(blank=True,null=True)
    description=models.TextField(blank=True, null=True)
    experience=models.CharField(max_length=500,blank=True, null=True)
    location=models.CharField(max_length=500,blank=True, null=True)
    posted_date=models.DateTimeField(auto_now_add=True)
    last_date=models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return self.title
    
class Careers(models.Model):
    header = models.CharField(max_length=1000, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    footer = models.CharField(max_length=500, blank=True, null=True)
    risec = models.CharField(max_length=6, blank=True, null=True) 

    @property
    def get_risec(self):
        ans = ''
        if self.risec:
            for i in self.risec:
                ans=ans+i+','
            return ans[:-1]
        else:
            return ans
        
class StartUpTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    startup = models.ForeignKey(StartUps,on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)  + '-' + str(self.startup)

class FileManager(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/documents')
    

    def __str__(self):
        return str(self.user.username) 

class UserRISECScore(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    marks = models.CharField(max_length=3)

    def __str__(self):
        return str(self.user.username) + '-' + str(self.marks)

    