from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from .forms import sign_form
from django.contrib.auth.models import User
# Create your views here.

def signup(request):
    form = sign_form()
    if request.method =='POST':
        form = sign_form(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect('home')

    return render(request,'signup.html',{'form':form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm

@login_required
def user_update_view(request):
    # Get the current user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('my_account')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'updateprofile.html', {'form': form})


