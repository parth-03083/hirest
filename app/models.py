from django.db import models

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

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return self.title
