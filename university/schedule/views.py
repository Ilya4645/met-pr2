from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import Teacher

def index(request):
    teachers = Teacher.objects.all()
    return render(request, 'index.html', {"teachers": teachers})

