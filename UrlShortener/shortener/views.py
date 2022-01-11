from django.shortcuts import render, redirect
import uuid
from . import models
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'index.html')

def create(requset):
    if requset.method =="POST":
        url = requset.POST['link']
        uid = str(uuid.uuid4())[:5]
        new_url = models.Url(link=url, uuid=uid)
        new_url.save()
        return HttpResponse(uid)

def go(request, pk):
    url_details = models.Url.objects.get(uuid=pk)
    return redirect(url_details.link)