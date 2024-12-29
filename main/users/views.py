from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, CustomPasswordChangeForm
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'



class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = 'done/'


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('product_list')
    else:
        form = UserRegisterForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
    else:
        form = UserLoginForm()
    return render(request, 'users/signin.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})

