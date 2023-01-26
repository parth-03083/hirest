from django.shortcuts import render

# Create your views here.
from .models import *

def indexView(request):
    jobs= Job.objects.all()
    context={'jobs':jobs}
    # print(jobs[0])
    return render(request,'home.html',context=context)