from django.shortcuts import render
import datetime as dt
from .models import User,tags
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import NewsLetterForm
# Create your views here.

def welcome(request):
    return render(request, 'all-instagram/index.html')

def welcome(request):

    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            recipient = NewsletterRecipients(name=name, email=email)
            recipient.save()
            send_welcome_email(name, email)

            HttpResponseRedirect('welcome')
    else:
        form = NewsLetterForm()

    return render (request, 'index.html', {"letterForm":form})

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