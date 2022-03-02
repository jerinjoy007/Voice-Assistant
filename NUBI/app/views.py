from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return HttpResponse("hello world")


def index1(request):
    return HttpResponse('Another response')


def index2(request):
    return render(request, 'index.html')
