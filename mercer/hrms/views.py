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
from django.contrib.auth.hashers import make_password
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


def StaffManage(request, page=1):#人员管理主页面
    loginform = LoginForm()
    username = request.user.username  # 获取当前登录的用户名
    department_list = Department.objects.filter(c_id=username)
    rank_list = Rank.objects.filter(c_id=username)
    stafflist = Employee.objects.filter(c_number=username)
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


def AddEmployee(request):  #添加员工
    username = request.user.username  # 获取当前登录的用户名
    request.encoding = 'utf-8'
    if request.method == 'POST':
        eindex = request.POST
        enumber = eindex.get('enumber')
        ename = eindex.get('ename')
        department = eindex.get('department')
        rank = eindex.get('rank')
        join_date = eindex.get('join_date')
        Employee.objects.create(number=enumber, name=ename, department=department, rank=rank, join_date=join_date,
                                c_number=username)
    return redirect('/hrms/staff')


def DeleteEmployee(request):  #删除员工
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


def EditEmployee(request, eid): #编辑员工信息
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


def PlanManage(request, page=1):#计划管理页面主页
    loginform = LoginForm()
    username = request.user.username  # 获取当前登录的用户名
    planlist = Plan.objects.order_by('id').all()
    per_page_count = 5  # 每页显示的个数
    endpage = planlist.count() / per_page_count + 1
    paginator = Paginator(planlist, per_page_count)  # 分页
    try:
        planlist = paginator.page(int(page))
    except PageNotAnInteger:
        planlist = paginator.page(1)
    except EmptyPage:
        planlist = paginator.page(paginator.num_pages)
    c = csrf(request)
    c.update({'planlist': planlist, 'loginform': loginform, 'endpage': endpage,})
    return render(request, 'PlanManage.html', context=c)


def PlanList(request, page=1): #授予记录页面
    loginform = LoginForm()
    username = request.user.username  # 获取当前登录的用户名
    planlist = Plan.objects.order_by('id').all()
    per_page_count = 5  # 每页显示的个数
    endpage = planlist.count() / per_page_count + 1
    paginator = Paginator(planlist, per_page_count)  # 分页
    try:
        planlist = paginator.page(int(page))
    except PageNotAnInteger:
        planlist = paginator.page(1)
    except EmptyPage:
        planlist = paginator.page(paginator.num_pages)
    c = csrf(request)
    c.update({'planlist': planlist, 'loginform': loginform, 'endpage': endpage,})
    return render(request, 'PlanList.html', context=c)


def AttributionList(request, page=1):
    loginform = LoginForm()
    username = request.user.username  # 获取当前登录的用户名
    planlist = Plan.objects.order_by('id').all()
    per_page_count = 5  # 每页显示的个数
    endpage = planlist.count() / per_page_count + 1
    paginator = Paginator(planlist, per_page_count)  # 分页
    try:
        planlist = paginator.page(int(page))
    except PageNotAnInteger:
        planlist = paginator.page(1)
    except EmptyPage:
        planlist = paginator.page(paginator.num_pages)
    c = csrf(request)
    c.update({'planlist': planlist, 'loginform': loginform, 'endpage': endpage,})
    return render(request, 'AttributionList.html', context=c)


def CompanyIndex(request):
    loginform = LoginForm()
    cname = request.user.username  # 获取当前登录的用户名
    departmentlist = Department.objects.filter(c_id=cname)
    ranklist = Rank.objects.filter(c_id=cname)
    company = NewUser.objects.get(username=cname)
    c = csrf(request)
    c.update({'departments': departmentlist, 'ranks': ranklist, 'loginform': loginform, 'company':company})
    return render(request, 'CompanyIndex.html', context=c)

def EditCompany(request):
    request.encoding = 'utf-8'
    if request.method == 'POST':
        cindex = request.POST
        cname = cindex.get('cname')
        cadd = cindex.get('cadd')
        cpwd = cindex.get('cpwd')
        NewUser.objects.filter(username=request.user.username).update(c_name=cname,password=make_password(cpwd), c_address=cadd)
    return redirect('/hrms/company')

def EditDepartment(request):
    request.encoding = 'utf-8'
    if request.method == 'POST':
        cindex = request.POST
        dname = cindex.get('dname')
        Department.objects.create(c_id=request.user.username,name=dname)
    return redirect('/hrms/company')

def DeleteDepartment(request):
    request.encoding = 'utf-8'
    if request.method == 'POST':
        department2del = request.POST.getlist('department2del')
        for sample in department2del:
            hehe = sample.split(':', 1)
            Department.objects.filter(number=hehe[0]).delete()  # 删除员工信息
    return redirect('/hrms/company')


def EditRank(request):
    request.encoding = 'utf-8'
    if request.method == 'POST':
        cindex = request.POST
        rname = cindex.get('rname')
        Rank.objects.create(c_id=request.user.username,name=rname)
    return redirect('/hrms/company')

def DeleteRank(request):
    request.encoding = 'utf-8'
    if request.method == 'POST':
        rank2del = request.POST.getlist('rank2del')
        for sample in rank2del:
            hehe = sample.split(':', 1)
            Rank.objects.filter(number=hehe[0]).delete()  # 删除员工信息
    return redirect('/hrms/company')


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
