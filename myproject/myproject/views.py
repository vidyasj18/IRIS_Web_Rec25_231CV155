from django.http import HttpResponse
from datetime import datetime, date
from django.http import JsonResponse

from django.shortcuts import render

def homepage(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

