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
from django.db.models import Q
from .models import NewUser
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_page
from .models import *
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from pyecharts import Bar, Line, Pie
import datetime
import time


# Create your views here.
def index(request):
    username = request.user.username  # 获取当前登录的用户名
    if username != '':
        userDL = NewUser.objects.get(username=username)
        last_date = userDL.last_login.strftime('%Y-%m-%d')  # 上次登录
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')  # 当前日期
        if time_cmp(last_date, now_time) < 0:
            attList = Attribution.objects.filter(c_name=username)
            for sample1 in attList:
                # 对归属情况进行更新
                if time_cmp(sample1.date, now_time) > 0:
                    is_allot = False
                    Attribution.objects.filter(id=sample1.id).update(is_allot=is_allot)
                else:
                    is_allot = True
                    Attribution.objects.filter(id=sample1.id).update(is_allot=is_allot)
            grantlist = Grant.objects.filter(c_name=username).order_by("id")
            for sample in grantlist:
                yiguishu = 0
                real_sum = 0
                attlist = Attribution.objects.filter(c_name=username, grant_name=sample.grant_name)
                for sample1 in attlist:
                    real_sum += sample1.real_sum
                    if sample1.is_allot == True:
                        yiguishu += sample1.real_sum
                weiguishu = real_sum - yiguishu
                Grant.objects.filter(id=sample.id).update(real_sum=real_sum, yiguishu=yiguishu, weiguishu=weiguishu)
    return render(request, 'index.html')


def StaffManage(request, page=1):  # 人员管理主页面
    loginform = LoginForm()
    username = request.user.username  # 获取当前登录的用户名
    department_list = Department.objects.filter(c_id=username)
    rank_list = Rank.objects.filter(c_id=username)
    stafflist = Employee.objects.filter(c_number=username).order_by("id")
    # 计算yishouyu yiguishu  weiguishu
    for sample in stafflist:
        attList = Attribution.objects.filter(c_name=username, e_id=sample.number)
        yishouyu = 0
        yiguishu = 0
        weiguishu = 0
        for sample1 in attList:
            # 对归属情况进行更新 迁移到首页了
            #
            yishouyu += int(sample1.real_sum)
            if sample1.is_allot == True:
                yiguishu += int(sample1.real_sum)
        weiguishu = yishouyu - yiguishu
        sample.yishouyu = yishouyu
        sample.yiguishu = yiguishu
        sample.weiguishu = weiguishu
    #
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


def AddEmployee(request):  # 添加员工
    username = request.user.username  # 获取当前登录的用户名
    request.encoding = 'utf-8'
    if request.method == 'POST':
        eindex = request.POST
        enumber = eindex.get('enumber')
        ename = eindex.get('ename')
        department = eindex.get('department')
        rank = eindex.get('rank')
        join_date = eindex.get('join_date')
        leave_date = eindex.get('leave_date')
        Employee.objects.create(number=enumber, name=ename, department=department, rank=rank, join_date=join_date,
                                leave_date=leave_date,
                                c_number=username)
    return redirect('/hrms/staff')


def DeleteEmployee(request):  # 删除员工
    request.encoding = 'utf-8'
    if request.method == 'POST':
        staff2del = request.POST.getlist('staff2del')
        for sample in staff2del:
            hehe = sample.split(':', 1)
            Employee.objects.filter(number=hehe[0]).delete()  # 删除员工信息
    return redirect('/hrms/staff')


def EmployeeIndex(request, eid):  # 查看单个员工页面
    loginform = LoginForm()
    employee = Employee.objects.get(number=eid, c_number=request.user.username)
    username = request.user.username  # 获取当前登录的用户名
    department_list = Department.objects.filter(c_id=username)
    rank_list = Rank.objects.filter(c_id=username)
    # 计算激励信息
    qq_ysy = 0
    qq_ygs = 0
    rsu_ysy = 0
    rsu_ygs = 0
    qq_att = Attribution.objects.filter(c_name=username, e_id=eid, tool='期权')
    for sample in qq_att:
        qq_ysy += sample.real_sum
        if sample.is_allot:
            qq_ygs += sample.real_sum
    qq_wgs = qq_ysy - qq_ygs
    rsu_att = Attribution.objects.filter(c_name=username, e_id=eid, tool='限制性股票')
    for sample in rsu_att:
        rsu_ysy += sample.real_sum
        if sample.is_allot:
            rsu_ygs += sample.real_sum
    rsu_wgs = rsu_ysy - rsu_ygs
    all_att = Attribution.objects.filter(c_name=username, e_id=eid).order_by('date')
    if len(all_att) > 0:
        nextDate = all_att[0].date
    else:
        nextDate = '暂无'
    # 计算授予详情
    guishu = Attribution.objects.filter(c_name=username, e_id=eid)
    grantlist = []
    for sample in guishu:
        one_grant = Grant.objects.get(grant_name=sample.grant_name, c_name=username)
        if one_grant not in grantlist:
            grantlist.append(one_grant)
    # 计算一次授予的实际授予量，已归属，未归属
    attlist = []
    for sample1 in grantlist:
        oneatt = Attribution.objects.filter(c_name=username, grant_name=sample1.grant_name, e_id=eid)
        attlist.append(oneatt)
        yiguishu = 0
        shijishouyu = 0
        for sample2 in oneatt:
            shijishouyu += sample2.real_sum
            if sample2.is_allot:
                yiguishu += sample2.real_sum
        weiguishu = shijishouyu - yiguishu
        sample1.one_real_sum = shijishouyu
        sample1.yiguishu = yiguishu
        sample1.weiguishu = weiguishu
    #
    c = csrf(request)
    c.update({'employee': employee, 'loginform': loginform, 'qq_ysy': qq_ysy, 'qq_ygs': qq_ygs, 'qq_wgs': qq_wgs,
              'department_list': department_list, 'rank_list': rank_list, 'grantlist': grantlist,
              'attlist': attlist, 'rsu_ysy': rsu_ysy, 'rsu_ygs': rsu_ygs, 'rsu_wgs': rsu_wgs, 'next_date': nextDate})
    return render(request, 'Employee.html', context=c)


def EditEmployee(request, eid):  # 编辑员工信息
    request.encoding = 'utf-8'
    if request.method == 'POST':
        eindex = request.POST
        ename = eindex.get('ename')
        department = eindex.get('department')
        rank = eindex.get('rank')
        join_date = eindex.get('join_date')
        leave_date = eindex.get('leave_date')
        Employee.objects.filter(number=eid).update(name=ename, department=department, rank=rank, join_date=join_date,
                                                   leave_date=leave_date)
    hehe = '/hrms/staff/employee/' + eid
    return redirect(hehe)

def SearchEmployee(request):
    if request.method == 'GET':
        eindex = request.GET
        ename = eindex.get('ename')
        enumber = eindex.get('enumber')
        edepartment = eindex.get('edepartment')
        erank = eindex.get('erank')
        employeelist = Employee.objects.filter(Q(name=ename)|Q(rank=erank)|Q(department=edepartment)|Q(number=enumber))
    c = csrf(request)
    c.update({'employeelist': employeelist})
    return render(request, 'StaffManage.html', context=c)

def SearchAttribution(request):
    if request.method == 'GET':
        eindex = request.GET
        ename = eindex.get('ename')
        enumber = eindex.get('enumber')
        edepartment = eindex.get('edepartment')
        erank = eindex.get('erank')
        attributionlist = Attribution.objects.filter(Q(e_name=ename)|Q(e_id=enumber))
    c = csrf(request)
    c.update({'attributionlist': attributionlist})
    return render(request, 'AttributionList.html', context=c)

def SearchPlan(request):
    if request.method == 'GET':
        eindex = request.GET
        gyear = eindex.get('gyear')
        pname = eindex.get('pname')
        gtool = eindex.get('gtool')
        sgrantlist = Grant.objects.filter(Q(g_time=gyear)|Q(grant_name=pname)|Q(tool=gtool))
    c = csrf(request)
    c.update({'sgrantlist': sgrantlist})
    return render(request, 'PlanList.html', context=c)


def time_cmp(first_time, second_time):
    begin_date = first_time.split('-')
    year1 = int(begin_date[0])
    month1 = int(begin_date[1])
    day1 = int(begin_date[2])
    begin_date = second_time.split('-')
    year2 = int(begin_date[0])
    month2 = int(begin_date[1])
    day2 = int(begin_date[2])
    if month1 < 10 and day1 < 10:
        date1 = str(year1) + '0' + str(month1) + '0' + str(day1)
    elif day1 < 10:
        date1 = str(year1) + str(month1) + '0' + str(day1)
    elif month1 < 10:
        date1 = str(year1) + '0' + str(month1) + str(day1)
    else:
        date1 = str(year1) + str(month1) + str(day1)
    if month2 < 10 and day2 < 10:
        date2 = str(year2) + '0' + str(month2) + '0' + str(day2)
    elif day2 < 10:
        date2 = str(year2) + str(month2) + '0' + str(day2)
    elif month2 < 10:
        date2 = str(year2) + '0' + str(month2) + str(day2)
    else:
        date2 = str(year2) + str(month2) + str(day2)
    return int(date1) - int(date2)


def EditEAtt(request, eid, att_id):  # 编辑员工归属信息
    request.encoding = 'utf-8'
    if request.method == 'POST':
        attindex = request.POST
        date = attindex.get('date')
        sum = attindex.get('sum')
        proportion = attindex.get('proportion')
        real_sum = int(float(proportion) * float(sum))
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')  # 当前日期
        if time_cmp(date, now_time) > 0:
            is_allot = False
        else:
            is_allot = True
        Attribution.objects.filter(id=att_id).update(date=date, sum=sum, proportion=proportion, real_sum=real_sum,
                                                     is_allot=is_allot)
    hehe = '/hrms/staff/employee/' + eid
    return redirect(hehe)


def DelEAtt(request, eid, att_id):  # 编辑员工归属信息
    request.encoding = 'utf-8'
    if request.method == 'POST':
        Attribution.objects.filter(id=att_id).delete()
    hehe = '/hrms/staff/employee/' + eid
    return redirect(hehe)


def PlanManage(request, page=1):  # 计划管理页面主页
    loginform = LoginForm()
    username = request.user.username  # 获取当前登录的用户名
    planlist = Plan.objects.filter(c_name=username).order_by("id")
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
    c.update({'planlist': planlist, 'loginform': loginform, 'endpage': endpage, })
    return render(request, 'PlanManage.html', context=c)


def AddthePlan(request):  # 新增授予
    username = request.user.username  # 获取当前登录的用户名
    request.encoding = 'utf-8'
    if request.method == 'POST':
        pindex = request.POST
        pname = pindex.get('pname')
        qq_sum = int(pindex.get('qq_sum'))
        rsu_sum = int(pindex.get('rsu_sum'))
        sum = qq_sum + rsu_sum
        validity_time = int(pindex.get('validity_time'))
        start_date = pindex.get('start_date')
        Plan.objects.create(c_name=username, name=pname, validity_time=validity_time, sum=sum, start_date=start_date,
                            qq_sum=qq_sum, rsu_sum=rsu_sum, rest_sum=sum, rest_qq_sum=qq_sum, rest_rsu_sum=rsu_sum)
    return redirect('/hrms/plan')


def AddPlan(request):
    username = request.user.username  # 获取当前登录的用户名
    stafflist = Employee.objects.filter(c_number=username).order_by("id")
    planlist = Plan.objects.filter(c_name=username).order_by("id")
    c = csrf(request)
    c.update({'staffs': stafflist, 'planlist': planlist})
    return render(request, 'AddPlan.html', context=c)


def AddAttribution(request):  # 新增授予
    username = request.user.username  # 获取当前登录的用户名
    request.encoding = 'utf-8'
    if request.method == 'POST':
        pindex = request.POST
        pname = pindex.get('pname')  # 计划名称
        start_date = pindex.get('start_date')  # 开始日期
        g_time = datetime.datetime.now().strftime('%Y-%m-%d')  # 授予日期
        tool = pindex.get('tool')  # 工具
        wait_time = pindex.get('wait_time')  # 等待期
        validity_time = pindex.get('validity_time')  # 有效期
        date = pindex.getlist('date')  # 日期和对应的比例
        proportion = pindex.getlist('proportion')
        att_fangshi = pindex.get('att_fangshi')  # 日期方式
        staff_index = pindex.getlist('staff_index')  # 员工
        staff_count = len(staff_index)  # 员工数量
        sum = pindex.get('sum')  # 每次授予量
        # 计算日期数量
        all_sum = int(sum) * int(staff_count) * (int(validity_time) - len(date))
        for sample in proportion:
            all_sum += int(float(sample) * float(sum)) * int(staff_count)
        one_sum = all_sum / int(staff_count)
        # 计划归属量在此之后不再更改，表示设定时的总量，实际授予总量在修改比例时更改  未归属量=实际授予量-已归属量
        # 计算授予的名称，授予的名称为计划名称+该企业该计划在授予表中出现的个数
        hehe = Grant.objects.filter(c_name=username, name=pname)
        grant_name = pname + 'zcy' + str(len(hehe))
        thisPlan = Plan.objects.get(c_name=username, name=pname)
        # 计算开始日期
        ss_date = start_date
        begin_date = ss_date.split('-')
        year = int(begin_date[0])
        month = int(begin_date[1])
        day = int(begin_date[2])
        month += int(wait_time)  # 等待期不超过12个月
        if month > 12:
            month = month - 12
        if att_fangshi == '年':
            year -= 1
        elif att_fangshi == '季':
            month -= 3
            if month < 1:
                month = month + 12
                year -= 1
        else:
            month -= 1
            if month <1 :
                month = month + 12
                year -= 1
        if month < 10 and day < 10:
            ss_date = str(year) + '-0' + str(month) + '-0' + str(day)
        elif day < 10:
            ss_date = str(year) + '-' + str(month) + '-0' + str(day)
        elif month < 10:
            ss_date = str(year) + '-0' + str(month) + '-' + str(day)
        else:
            ss_date = str(year) + '-' + str(month) + '-' + str(day)
        for one_e in staff_index:
            hehe = one_e.split(':', 1)
            e_id = hehe[0]
            e_name = hehe[1]
            hehe_date = ss_date
            xhcs = int(validity_time) - len(date)
            while xhcs > 0:
                # 计算日期
                begin_date = hehe_date.split('-')
                year = int(begin_date[0])
                month = int(begin_date[1])
                day = int(begin_date[2])
                if att_fangshi == '年':
                    year += 1
                elif att_fangshi == '季':
                    month += 3
                    if month > 12:
                        month = month - 12
                        year += 1
                else:
                    month += 1
                    if month > 12:
                        month = month - 12
                        year += 1
                if month < 10 and day < 10:
                    hehe_date = str(year) + '-0' + str(month) + '-0' + str(day)
                elif day < 10:
                    hehe_date = str(year) + '-' + str(month) + '-0' + str(day)
                elif month < 10:
                    hehe_date = str(year) + '-0' + str(month) + '-' + str(day)
                else:
                    hehe_date = str(year) + '-' + str(month) + '-' + str(day)
                if hehe_date in date:
                    xhcs += 1
                else:
                    Attribution.objects.create(plan_name=pname, c_name=username, grant_name=grant_name, e_id=e_id,
                                               real_sum=int(sum), tool=tool,
                                               e_name=e_name, date=hehe_date, sum=int(sum), proportion=1,
                                               att_fangshi=att_fangshi)
                xhcs -= 1
            for (one_date, one_pro) in zip(date, proportion):
                begin_date = one_date.split('-')
                year = int(begin_date[0])
                month = int(begin_date[1])
                day1 = day
                if month < 10 and day < 10:
                    hehe_date = str(year) + '-0' + str(month) + '-0' + str(day1)
                elif day < 10:
                    hehe_date = str(year) + '-' + str(month) + '-0' + str(day1)
                elif month < 10:
                    hehe_date = str(year) + '-0' + str(month) + '-' + str(day1)
                else:
                    hehe_date = str(year) + '-' + str(month) + '-' + str(day1)
                yes = float(sum)
                yes2 = float(one_pro)
                yes3 = int(yes * yes2)
                Attribution.objects.create(plan_name=pname, c_name=username, grant_name=grant_name, e_id=e_id,
                                           real_sum=yes3, tool=tool,
                                           e_name=e_name, date=hehe_date, sum=int(yes), proportion=yes2,
                                           att_fangshi=att_fangshi)

        staff_renci = Attribution.objects.filter(plan_name=pname, c_name=username).values('e_id').distinct()
        if tool == '期权':
            Plan.objects.filter(c_name=username, name=pname).update(real_sum=int(thisPlan.real_sum) + all_sum,
                                                                    rest_sum=int(thisPlan.rest_sum) - all_sum,
                                                                    real_qq_sum=int(thisPlan.real_qq_sum) + all_sum,
                                                                    rest_qq_sum=int(thisPlan.rest_qq_sum) - all_sum,
                                                                    count=int(thisPlan.count) + staff_count,
                                                                    count_renci=len(staff_renci))
        else:  # 人数不去重，人次去重
            Plan.objects.filter(c_name=username, name=pname).update(real_sum=int(thisPlan.real_sum) + all_sum,
                                                                    rest_sum=int(thisPlan.rest_sum) - all_sum,
                                                                    real_rsu_sum=int(thisPlan.real_qq_sum) + all_sum,
                                                                    rest_rsu_sum=int(thisPlan.rest_qq_sum) - all_sum,
                                                                    count=int(thisPlan.count) + staff_count,
                                                                    count_renci=len(staff_renci))
        Grant.objects.create(c_name=username, name=pname, g_time=g_time, start_date=start_date, tool=tool, sum=all_sum,
                             real_sum=all_sum, yiguishu=0, rest_sum=all_sum, grant_name=grant_name, onesum=one_sum,
                             validity_time=validity_time, weiguishu=0, count=staff_count, wait_time=wait_time)
    return redirect('/hrms/planlist')


def PlanList(request, page=1):  # 授予记录页面
    loginform = LoginForm()
    username = request.user.username  # 获取当前登录的用户名
    grantlist = Grant.objects.filter(c_name=username).order_by("id")
    per_page_count = 5  # 每页显示的个数
    endpage = grantlist.count() / per_page_count + 1
    paginator = Paginator(grantlist, per_page_count)  # 分页
    try:
        grantlist = paginator.page(int(page))
    except PageNotAnInteger:
        grantlist = paginator.page(1)
    except EmptyPage:
        grantlist = paginator.page(paginator.num_pages)
    c = csrf(request)
    c.update({'grantlist': grantlist, 'loginform': loginform, 'endpage': endpage, })
    return render(request, 'PlanList.html', context=c)


def AttributionList(request, page=1):
    loginform = LoginForm()
    username = request.user.username  # 获取当前登录的用户名
    attlist = Attribution.objects.filter(c_name=username, is_allot=True).order_by("date")
    per_page_count = 5  # 每页显示的个数
    endpage = attlist.count() / per_page_count + 1
    paginator = Paginator(attlist, per_page_count)  # 分页
    try:
        attlist = paginator.page(int(page))
    except PageNotAnInteger:
        attlist = paginator.page(1)
    except EmptyPage:
        attlist = paginator.page(paginator.num_pages)
    c = csrf(request)
    c.update({'attlist': attlist, 'loginform': loginform, 'endpage': endpage, })
    return render(request, 'AttributionList.html', context=c)


def CompanyIndex(request):
    loginform = LoginForm()
    cname = request.user.username  # 获取当前登录的用户名
    departmentlist = Department.objects.filter(c_id=cname)
    ranklist = Rank.objects.filter(c_id=cname)
    company = NewUser.objects.get(username=cname)
    c = csrf(request)
    c.update({'departments': departmentlist, 'ranks': ranklist, 'loginform': loginform, 'company': company})
    return render(request, 'CompanyIndex.html', context=c)


def EditCompany(request):
    request.encoding = 'utf-8'
    if request.method == 'POST':
        cindex = request.POST
        cname = cindex.get('cname')
        cadd = cindex.get('cadd')
        cpwd = cindex.get('cpwd')
        NewUser.objects.filter(username=request.user.username).update(c_name=cname, password=make_password(cpwd),
                                                                      c_address=cadd)
    return redirect('/hrms/')


def EditDepartment(request):
    request.encoding = 'utf-8'
    if request.method == 'POST':
        cindex = request.POST
        dname = cindex.get('dname')
        Department.objects.create(c_id=request.user.username, name=dname)
    return redirect('/hrms/company')


def DeleteDepartment(request):
    request.encoding = 'utf-8'
    if request.method == 'POST':
        department2del = request.POST.getlist('department2del')
        for sample in department2del:
            Department.objects.filter(name=sample).delete()  # 删除员工信息
    return redirect('/hrms/company')


def EditRank(request):
    request.encoding = 'utf-8'
    if request.method == 'POST':
        cindex = request.POST
        rname = cindex.get('rname')
        Rank.objects.create(c_id=request.user.username, name=rname)
    return redirect('/hrms/company')


def DeleteRank(request):
    request.encoding = 'utf-8'
    if request.method == 'POST':
        rank2del = request.POST.getlist('rank2del')
        for sample in rank2del:
            Rank.objects.filter(name=sample).delete()  # 删除员工信息
    return redirect('/hrms/company')


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
