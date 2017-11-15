from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegistrationForm
from accounts.models import Account

# Create your views here.
def get_index(request):
    return render(request, "index.html")
    
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect(get_index)
    
def login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data["username"],
                                     password=form.cleaned_data["password"])
                                     
            if user is not None:
                auth.login(request, user)
                messages.error(request, "You have succesfully logged in")
                
                if request.GET and request.GET['next'] !='':
                    next = request.GET['next']
                    return HttpResponseRedirect(next)
                else:
                    return redirect(profile)
                    
            else:
                form.add_error(None, "Your username or password was not registered") #error message not working. will come back to it
            
    else:
        form = UserLoginForm()
        
    return render(request, "login.html", {"form" : form})
    
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            user = auth.authenticate(username=form.cleaned_data["username"],
                                     password=form.cleaned_data["password1"])
            
            if user is not None:
                auth.login(request, user)
                return redirect(get_index)
    else:
        form = UserRegistrationForm()
        
    return render(request, "register.html", {"form" : form})
    
@login_required(login_url="/accounts/login") #this url link must be hard coded unlike the other urs such as <a href="{% url "login" %}">
def profile(request):
    return render(request, "profile.html")