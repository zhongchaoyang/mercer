# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
from django.http import JsonResponse
# 导入render和HttpResponse模块
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
# 导入Paginator,EmptyPage和PageNotAnInteger模块
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.context_processors import csrf
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import NewUser
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_page
from .models import *
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from pyecharts import Bar, Line, Pie
import time


# Create your views here.
def index(request):
    return render(request, 'index.html')


def StaffManage(request, page=1):
    loginform = LoginForm()
    username = request.user.username  # 获取当前登录的用户名
    department_list = Department.objects.filter(c_id=username)
    rank_list = Rank.objects.filter(c_id=username)
    stafflist = Employee.objects.order_by('number').all()
    per_page_count = 5  # 每页显示的个数
    endpage = stafflist.count() / per_page_count + 1
    paginator = Paginator(stafflist, per_page_count)  # 分页
    try:
        stafflist = paginator.page(int(page))
    except PageNotAnInteger:
        stafflist = paginator.page(1)
    except EmptyPage:
        stafflist = paginator.page(paginator.num_pages)
    c = csrf(request)
    yishouyu = '1'
    yiguishu = '2'
    weiguishu = '0'
    c.update({'staffs': stafflist, 'loginform': loginform, 'endpage': endpage,
              'department_list': department_list, 'rank_list': rank_list,
              'yishouyu': yishouyu, 'yiguishu': yiguishu, 'weiguishu': weiguishu})
    return render(request, 'StaffManage.html', context=c)


def AddEmployee(request):
    request.encoding = 'utf-8'
    if request.method == 'POST':
        eindex = request.POST
        enumber = eindex.get('enumber')
        ename = eindex.get('ename')
        department = eindex.get('department')
        rank = eindex.get('rank')
        join_date = eindex.get('join_date')
        Employee.objects.create(number=enumber, name=ename, department=department, rank=rank, join_date=join_date)
    return redirect('/hrms/staff')


def DeleteEmployee(request):
    request.encoding = 'utf-8'
    if request.method == 'POST':
        staff2del = request.POST.getlist('staff2del')
        for sample in staff2del:
            hehe = sample.split(':', 1)
            Employee.objects.filter(number=hehe[0]).delete()  # 删除员工信息
    return redirect('/hrms/staff')


def EmployeeIndex(request, eid):  # 查看单个员工页面
    loginform = LoginForm()
    employee = Employee.objects.get(number=eid)
    username = request.user.username  # 获取当前登录的用户名
    department_list = Department.objects.filter(c_id=username)
    rank_list = Rank.objects.filter(c_id=username)
    c = csrf(request)
    c.update({'employee': employee, 'loginform': loginform,
              'department_list': department_list, 'rank_list': rank_list})
    return render(request, 'Employee.html', context=c)


def EditEmployee(request, eid):
    request.encoding = 'utf-8'
    if request.method == 'POST':
        eindex = request.POST
        ename = eindex.get('ename')
        department = eindex.get('department')
        rank = eindex.get('rank')
        join_date = eindex.get('join_date')
        Employee.objects.filter(number= eid).update(name=ename,department = department, rank = rank,join_date = join_date)
    hehe = '/hrms/staff/employee/'+eid
    return redirect(hehe)


def PlanManage(request):
    return render(request, 'PlanManage.html')


def PlanList(request):
    return render(request, 'PlanList.html')


def AttributionList(request):
    return render(request, 'AttributionList.html')


def CompanyIndex(request):
    return render(request, 'CompanyIndex.html')


def AddPlan(request):
    return render(request, 'AddPlan.html')


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
                user = NewUser.objects.create_superuser(username=username, email=email, password=password, c_name=cname,
                                                        c_address=caddress)
                user.save()
                login(request, user)
                url = request.POST.get('source_url', '/hrms/')
                return redirect(url)
            # return render(request, 'login.html', {'success': "you have successfully registered!"})                    return redirect('/website/login')
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
