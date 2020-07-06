from django.shortcuts import render,redirect,get_object_or_404
import datetime as dt
from .models import tags,Profile,Comment,Post,User
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import NewsLetterForm,PostForm,CommentForm,ProfileForm
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def welcome(request):
    return render(request, 'all-instagram/index.html')

@login_required(login_url='/accounts/login/')
def welcome(request):
    images = Post.objects.all()
    profiles= Profile.objects.all()
    print(profiles)
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
    return render(request, 'edit.html', {"profileform":new_profile})

@login_required(login_url='/accounts/login/')
def user(request, user_id):
    user_object=get_object_or_404(User, pk=user_id)
    commentform = CommentForm()
    if request.user == user_object:
        return redirect('profile')
    user_images = user_object.posts.all()
    return render(request, 'userprofile.html')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['image', 'post_caption']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url="/"

@login_required(login_url='/accounts/login/')
def comment(request, post_id):
    commentform = CommentForm()
    comments=Comment.objects.all()
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.photo = post
            comment.save()
            return redirect('/')
    else:
        form = CommentForm()
    return redirect(request, 'index.html',{"commentform":commentform, "comments":comments})

@login_required(login_url='/accounts/login/')
def likePost(request,image_id):

    image = Post.objects.get(pk = image_id)

    is_liked = False
    if image.likes.filter(id = request.user.id).exists():
        image.likes.remove(request.user)
        is_liked = False
    else:
        image.likes.add(request.user)
        is_liked = True

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))