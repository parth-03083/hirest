from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Skills(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MyProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=13,blank=True, null=True)
    skills = models.ManyToManyField(Skills,blank=True)
    current_job=models.CharField(max_length=100)
    education = models.TextField(blank=True,null=True)
    total_experience = models.CharField(max_length=10,blank=True,null=True)
    experties = models.IntegerChoices('experties', 'Beginner Intermediate Expert')

    def __str__(self):
        return self.user.username


class Job(models.Model):
    title=models.CharField(max_length=500,blank=True, null=True)
    company_Name=models.CharField(max_length=500,blank=True, null=True)
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

class AppliedJobs(models.Model):
    job=models.ForeignKey(Job,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    applied_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job.title + '-' + self.user.username

class StartUps(models.Model):
    name=models.CharField(max_length=500,blank=True, null=True)
    description=models.TextField(blank=True, null=True)
    location=models.CharField(max_length=500,blank=True, null=True)
    logo=models.ImageField(upload_to='uploads/startup/',blank=True, null=True)
    website=models.CharField(max_length=500,blank=True, null=True)
    email=models.EmailField(blank=True, null=True)
    phone=models.CharField(max_length=500,blank=True, null=True)
    founded_date=models.DateTimeField(blank=True, null=True)
    last_date=models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class Internships(models.Model):
    title=models.CharField(max_length=500,blank=True, null=True)
    company_Name=models.CharField(max_length=500,blank=True, null=True)
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