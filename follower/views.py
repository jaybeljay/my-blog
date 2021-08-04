from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import CreateUserForm


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('posts_list')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account was successfully created!')
                return redirect('login')
            else:
                print(form.errors)
        
        return render(request, 'register.html', {'form': form})
    

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('posts_list')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('posts_list')
            else:
                messages.info(request, 'Username or password is incorrect')
                return render(request, 'login.html')
                
        return render(request, 'login.html')
    

def logoutPage(request):
    logout(request)
    return redirect('login')
