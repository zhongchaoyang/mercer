# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from mercer import settings

# Create your models here.

@python_2_unicode_compatible
class NewUser(AbstractUser):  #企业表
    c_name = models.CharField('c_name', default='', max_length=256)
    c_address = models.CharField('c_address', default='', max_length=256)
    profile = models.CharField('profile', default='', max_length=256)
    def __str__(self):
        return self.username


class Department(models.Model):#部门表
    c_id = models.CharField('c_id', default='',max_length=256)
    name = models.CharField('name', default='',max_length=256)
    def __str__(self):
        return self.name.encode('utf-8')


class Rank(models.Model):#职级表
    c_id = models.CharField('c_id', default='',max_length=256)
    name = models.CharField('name', default='',max_length=256)
    def __str__(self):
        return self.name.encode('utf-8')


class Employee(models.Model):   #员工表
    number = models.CharField('number', default='', max_length=256) #工号
    name = models.CharField('name', default='', max_length=256) #员工姓名
    join_date = models.CharField('join_date', default='', max_length=256) #入职时间
    leave_date = models.CharField('leave_date', default='', max_length=256) #离职时间
    department = models.CharField('department', default='', max_length=256) #部门
    rank = models.CharField('rank', default='', max_length=256) #职级
    is_finish = models.BooleanField('is_finish', default=True)  #是否完成业绩指标
    c_number = models.CharField('c_number', default='', max_length=256) #企业编号
    #额外添加
    yishouyu = models.CharField('yishouyu', default='', max_length=256)
    yiguishu = models.CharField('yiguishu', default='', max_length=256)
    weiguishu = models.CharField('weiguishu', default='', max_length=256)


    def __str__(self):
        return self.number


class Plan(models.Model):
    c_name = models.CharField('c_name', default='', max_length=256) #对应企业
    name = models.CharField('name', default='', max_length=256) #计划名称
    start_date = models.CharField('start_date', default='', max_length=256)#开始实施时间
    validity_time = models.FloatField('validity_time',default= 0.0)#有效期
    sum = models.FloatField('sum',default= 0.0)#计划总量
    g_time = models.CharField('g_time', default='', max_length=256)#授予日期
    tool = models.CharField('tool',default='',max_length=256)#使用的工具
    count = models.IntegerField('count', default=0)#计划覆盖的人数
    onesum = models.FloatField("onesum",default=0.0)
    #额外变化量
    yiguishu = models.FloatField("yiguishu",default=0.0)#已归属量
    weiguishu = models.FloatField("weiguishu",default=0.0)#已归属量
    now_sum = models.FloatField('now_sum', default=0.0)  # 实际授予总量
    rest_sum = models.FloatField('rest_sum', default=0.0)  # 剩余总量
    def __str__(self):
        return self.name.encode('utf-8')


class Attribution(models.Model):
    plan_name = models.CharField('plan_name', default='', max_length=256)  # 计划名称
    c_id = models.CharField('c_id', default='', max_length=256)  # 对应企业
    e_id = models.CharField('e_id',default='',max_length=256)#对应员工
    e_name = models.CharField('name', default='', max_length=256)  # 员工姓名
    date = models.CharField('date', default='', max_length=256)#开始日期
    sum = models.FloatField("sum",default=0.0)#已归属量
    proportion = models.FloatField('proportion',default=0.0)#分配系数
    att_fangshi = models.CharField('att_fangshi', default='', max_length=256)#归属方式
    is_allot = models.BooleanField('is_allot',default=False) #是否已经归属

    def __str__(self):
        return self.plan_name.encode('utf-8')