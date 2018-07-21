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
    url(r'^staff/edit_att/(?P<eid>(.*?))-(?P<att_id>(.*?))/$', views.EditEAtt, name='editA'),  # 编辑员工归属信息
    url(r'^staff/page/(\d+)/$', views.StaffManage),

    url(r'^plan/$', views.PlanManage, name='plan'),
    url(r'^plan/page/(\d+)/$', views.PlanManage),
    url(r'^addplan/$', views.AddPlan, name='addplan'),

    url(r'^planlist/$', views.PlanList, name='planlist'),
    url(r'^planlist/page/(\d+)/$', views.PlanList),

    url(r'^attlist/$', views.AttributionList, name='attlist'),
    url(r'^attlist/page/(\d+)/$', views.AttributionList),

    url(r'^company/$', views.CompanyIndex, name='company'),
    url(r'^company/editcompany$', views.EditCompany, name='editcompany'),  # 修改企业信息
    url(r'^company/editdepartment$', views.EditDepartment, name='editdepartment'),  # 编辑部门
    url(r'^company/editrank$', views.EditRank, name='editrank'),  # 编辑职级
    url(r'^company/deletedepartment$', views.DeleteDepartment, name='deletedepartment'),  # 编辑部门
    url(r'^company/deleterank$', views.DeleteRank, name='deleterank'),  # 编辑职级
]