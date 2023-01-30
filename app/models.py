from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Skills(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name



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
