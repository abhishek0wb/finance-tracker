from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = SimpleUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('expenses:dashboard')
    else:
        form = SimpleUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

class SimpleUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('expenses:dashboard')  # Redirects to dashboard
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('users:login')  # Use app_name:view_name