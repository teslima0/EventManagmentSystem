from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm 
from .forms import ResgisterUserForm

# Create your views here.
def login_user(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect ('homepage')

        else:
            messages.success(request,("Wrong username or password, try again..."))
            return redirect ('loginpage')


    else:

        return render(request, 'authenticate/login.html', {})


def Register_user(request):
    if request.method=="POST":
        #form=UserCreationForm(request.POST)
        form=ResgisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username, password=password)
            login(request,user)
            messages.success(request,('Registration successful'))
            return redirect('homepage')
    else:
            form=ResgisterUserForm()
    return render(request, 'authenticate/register_user.html', {'form':form})

def logout_user(request):
    logout(request)
    messages.success(request,("You have logged out"))
    return redirect ('homepage')
