from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from hustle.models import Hustle
from .models import Profile
from django.contrib.auth.models import User

def registration(request):
    if request.method == "POST":
        form = UserRegForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account Created for {username}!')
            return redirect('login')
    else:
        form = UserRegForm()
    return render(request, "register.html", {"form": form})


@login_required
def user_profile(request, username, **kwargs):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404
    object = Hustle.objects.filter(user=user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST or None, instance=request.user)
        p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Profile Has Been Updated!')
            return HttpResponseRedirect(request.path_info)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        "u_form": u_form,
        "p_form": p_form,
        "user": user,
        "object": object,
    }
    return render(request, "profile.html", context)


