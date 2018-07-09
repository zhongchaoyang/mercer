# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
from django.http import JsonResponse
# 导入render和HttpResponse模块
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
# 导入Paginator,EmptyPage和PageNotAnInteger模块
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import NewUser
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_page
from .models import *
from django.http import HttpResponse
from pyecharts import Bar, Line, Pie
import time
# Create your views here.
def index(request):
    return render(request, 'index3.html')


def StaffManage(request):
    return render(request, 'StaffManage.html')


def PlanManage(request):
    return render(request, 'PlanManage.html')


def CompanyIndex(request):
    return render(request, 'CompanyIndex.html')


def log_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['uid']
            password = form.cleaned_data['pwd']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                url = request.POST.get('source_url', '/hrms/')
                return redirect(url)
            else:
                return render(request, 'login.html', {'form': form, 'error': "password or username is not ture!"})

        else:
            return render(request, 'login.html', {'form': form})


@login_required
def log_out(request):
    url = request.POST.get('source_url', '/hrms/')
    logout(request)
    return redirect(url)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['uid']
            password = form.cleaned_data['pwd']
            email = form.cleaned_data['eml']
            cname = form.cleaned_data['cname']
            caddress = form.cleaned_data['cad']
            user = authenticate(username=username, password=password)
            if user:
                return render(request, 'register.html', {'form': form, 'error': "password or username was registered!"})
            else:
                user = NewUser.objects.create_superuser(username=username, email=email, password=password, c_name=cname, c_address=caddress)
                user.save()
                login(request, user)
                url = request.POST.get('source_url', '/hrms/')
                return redirect(url)
            # return render(request, 'login.html', {'success': "you have successfully registered!"})                    return redirect('/website/login')
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})