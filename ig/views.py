from django.shortcuts import render,redirect
import datetime as dt
from .models import tags,Profile,Comment,Post,User
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import NewsLetterForm,PostForm,CommentForm,ProfileForm
# Create your views here.

def welcome(request):
    return render(request, 'all-instagram/index.html')

def welcome(request):
    images = Post.objects.all()
    profiles= Profile.objects.all()
    commentform = CommentForm()


    if request.method == 'POST':
        form = NewsLetterForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            recipient = NewsletterRecipients(name=name, email=email)
            recipient.save()
            send_welcome_email(name, email)
            request.user.post(form)

            HttpResponseRedirect('welcome')
    else:
        form = NewsLetterForm()

    return render (request, 'index.html', {"images":images,"profiles":profiles, "letterForm":form, "commentform":commentform})

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'profile' in request.GET and request.GET["profile"]:
        search_term = request.GET.get("profile")
        searched_profiles = Profile.search_by_user(search_term)
        message=f"{search_term}"

        return render(request,'search.html',{"message":message,"profiles":searched_profiles})

    else:
        message="You haven't searched for any term"

       return render(request,'search.html')

@login_required(login_url='/accounts/login/')
def profile(request):
    images = request.user.posts.all()
    user_object = request.user
    user_images = user_object.posts.all()
    commentform = CommentForm()
    comments=Comment.objects.all()
    return render(request, 'profile.html')

@login_required(login_url='/accounts/login/')
def edit(request):
    if request.method == 'POST':
        print(request.FILES)
        new_profile = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if new_profile.is_valid():
            new_profile.save()
            print(new_profile.fields)
            return redirect('profile')
    else:
        new_profile = ProfileForm(instance=request.user.profile)
    return render(request, 'edit.html')

