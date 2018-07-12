from django.conf.urls import include,url
from hrms import views


urlpatterns = [
    url(r'^$',views.index, name='index'),

    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^register/$', views.register, name='register'),

    url(r'^staff/$', views.StaffManage, name='staff'),
    url(r'^staff/(\d+)/$', views.StaffManage),
    url(r'^plan/$', views.PlanManage, name='plan'),
    url(r'^planlist/$', views.PlanList, name='planlist'),
    url(r'^addplan/$', views.AddPlan, name='addplan'),
    url(r'^attlist/$', views.AttributionList, name='attlist'),
    url(r'^company/$', views.CompanyIndex, name='company'),
]