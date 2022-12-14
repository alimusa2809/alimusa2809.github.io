from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from.forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from.models import Profile

def loginUser(request):
    page = 'login'
    context = {'login' : login}
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            User.objects.get(username = username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or Password is Incorrect')

    return render(request, 'users/login_register.html', context)

def logoutUser(request):
    logout(request)
    messages.success(request, 'User was Logged out.')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    context = {'page': page, 'form': form}
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User Account was created!')
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/login_register.html', context)


# Create your views here.
def profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles':profiles
    }
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    #tags = projects.tag.all()
    context = {'profile': profile, 'skills': skills, 'projects': projects}

    return render(request, 'users/user-profile.html', context)