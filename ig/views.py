from django.shortcuts import render
import datetime as dt
from .models import Editor,Profile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def welcome(request):
    return render(request, 'all-instagram/index.html')


@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'profile' in request.GET and request.GET["profile"]:
        search_term = request.GET.get("profile")
        searched_profiles = Profile.search_by_user(search_term)
        message=f"{search_term}"

        return render(request,'search.html',{"message":message,"profiles":searched_profiles})

    else:
        message="You haven't searched for any term"

    return render(request,'search.html',locals()) 