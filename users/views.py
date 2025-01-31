from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User

# Create your views here.
from users.forms import LoginForm, SignUpForm, ProfileEditForm


def dashboard(request):
    user = request.user
    if user.is_anonymous:
        return redirect('login')
    if user.is_admin():
        return redirect('tasks:admin_task_list')
    if user.is_user():
        return redirect('tasks:task_list')


def user_login(request):
    next = request.GET.get('next', None)
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(data=request.POST or None)
    context = {
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(username=email, password=password)
            if user is None:
                messages.error(request, "Invalid login credentials")
                templates = 'users/login.html'
                return render(request, templates, context)
            else:
                login(request, user)
                if next:
                    return redirect(next)
                messages.success(request, 'Successfully logged in!')
                return redirect('dashboard')
    templates = 'users/login.html'
    return render(request, templates, context)


def user_signup(request):
    form = SignUpForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.role = 'user'
            instance.save()
            password = form.cleaned_data['password1']
            instance.set_password(password)
            instance.save()
            messages.success(request, 'sign up successfully'.format(instance.first_name))
            return redirect('login')
    template_name = "users/signup.html"
    return render(request, template_name, {'form': form})


@login_required
def profile_edit_view(request, id=None):
    instance = get_object_or_404(User, id=id)
    form = ProfileEditForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect("dashboard")
    template_name = "users/profile_edit.html"
    context = {
        "form": form,
    }
    return render(request, template_name, context)


def user_logout(request):
    """
    Logout a user
    """
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('login')
