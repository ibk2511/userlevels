from django.forms import ModelForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from .decoraters import *


# Create your views here.
@login_required(login_url='login')
@admin_only
def homepage(request):
    admins = adminlevel.objects.all()
    context = {'admins': admins}
    return render(request, 'main/dashboard.html', context)


def login(request):
    return HttpResponse("hello login here")


def register(request):
    if request.method == 'POST':
        if request.POST['password1'] != request.POST['password2']:
            messages.error(request, "Passwords don't match")
            return render(request, 'main/register.html')
        else:
            try:
                user_exists = User.objects.get(email=request.POST['email'])
            except Exception as e:
                print(e)
                user_exists = None
            if user_exists:
                messages.error(request, 'There already exists a user with the given email')
            elif user_exists is None:
                password = request.POST.get('password2')
                user = User.objects.create_user(
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=password,
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name']
                )
                if request.POST['user-type'] == 'admin2':
                    adminlevel.objects.create(user=user)
                    messages.success(request, 'You have been successfully registered')
                    group = Group.objects.get(name='admin2')
                    user.groups.add(group)
                    return render(request, 'main/userstatus.html')
                elif request.POST['user-type'] == 'admin3':
                    adminlevel.objects.create(user=user)
                    messages.success(request,
                                     'You have been successfully registered as a level 2')
                    group = Group.objects.get(name='admin3')
                    user.groups.add(group)
                    return render(request, 'main/userstatus.html')


    else:
        return render(request, "main/register.html")


class CreationForm(ModelForm):
    class Meta:
        model = publish
        exclude = ('is_accept',)

def userPage(request):
    if request.method == "POST":
        data = request.POST.copy()
        data['user'] = request.user
        populated_form = CreationForm(data, request.FILES)
        print(populated_form)
        print(populated_form.errors)
        if populated_form.is_valid():
            populated_form.save()
            messages.success(request, 'admin data Saved successfully')
        return render(request, 'main/userhome.html')

    return render(request, 'main/userpage.html')


def interuserPage(request):
    return render(request, 'main/interuserpage.html')


def admin_accept(request, id):
    user = adminlevel.objects.get(id=id)
    user.is_accept = True
    user.save()
    messages.info(request, "user accepted successfully")
    return redirect(homepage)


def admin_reject(request, id):
    user = adminlevel.objects.get(id=id)
    user.is_reject = True
    print(user)
    user.save()
    messages.info(request, "user rejected successfully")
    return redirect(homepage)
