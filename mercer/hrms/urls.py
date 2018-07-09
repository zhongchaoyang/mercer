from django.conf.urls import include,url
from hrms import views


urlpatterns = [
    url(r'^$',views.index, name='index'),

    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^register/$', views.register, name='register'),

    url(r'^staff/$', views.StaffManage, name='staff'),
    url(r'^plan/$', views.PlanManage, name='plan'),
    url(r'^company/$', views.CompanyIndex, name='company'),
]