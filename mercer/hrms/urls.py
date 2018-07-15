# -*- coding: utf-8 -*-
from django.conf.urls import include,url
from hrms import views


urlpatterns = [
    url(r'^$',views.index, name='index'),

    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^register/$', views.register, name='register'),

    url(r'^staff/$', views.StaffManage, name='staff'),
    url(r'^staff/adde$', views.AddEmployee, name='adde'),#添加员工
    url(r'^staff/dele$', views.DeleteEmployee, name='dele'),  # 删除员工
    url(r'^staff/employee/(?P<eid>(.*?))/$', views.EmployeeIndex, name='eIndex'),#查询具体员工信息
    url(r'^staff/edit/(?P<eid>(.*?))/$', views.EditEmployee, name='editE'),  # 编辑员工信息
    url(r'^staff/page/(\d+)/$', views.StaffManage),

    url(r'^plan/$', views.PlanManage, name='plan'),
    url(r'^plan/page/(\d+)/$', views.PlanManage),

    url(r'^planlist/$', views.PlanList, name='planlist'),
    url(r'^addplan/$', views.AddPlan, name='addplan'),
    url(r'^attlist/$', views.AttributionList, name='attlist'),
    url(r'^company/$', views.CompanyIndex, name='company'),
]