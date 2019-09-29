from django.urls import include, path, re_path
from django.conf.urls import url
from django.contrib import admin
from makeReports import views
from django.contrib.auth import views as auth_views
app_name = "makeReports"
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    #SLO Urls
    re_path(r'^report/(?P<report>\d+)/slo/summary/$', views.SLOSummary.as_view(), name='slo-summary'),
    re_path(r'^report/(?P<report>\d+)/slo/add/$', views.AddNewSLO.as_view(), name='add-slo'),
    re_path(r'^report/(?P<report>\d+)/slo/import/$', views.ImportSLO.as_view(), name='import-slo'),
    re_path(r'^report/(?P<report>\d+)/slo/edit/new/(?P<sloIR>\d+)/$', views.EditNewSLO.as_view(), name='edit-new-slo'),
    re_path(r'^report/(?P<report>\d+)/slo/edit/impt/(?P<sloIR>\d+)/$', views.EditImportedSLO.as_view(), name='edit-impt-slo'),
    re_path(r'^report/(?P<report>\d+)/slo/stakeholders/$', views.StakeholderEntry.as_view(), name='slo-stakeholders'),
    #AAC Admin URLS
    re_path(r'^aac/home/$', views.AdminHome.as_view(), name='admin-home'),
    re_path(r'^aac/college/create/$',views.CreateCollege.as_view(), name="add-college"),
    re_path(r'^aac/college/update/(?P<pk>\d+)/$', views.UpdateCollege.as_view(), name='update-college'),
    re_path(r'^aac/college/list/$', views.CollegeList.as_view(), name='college-list'),
    re_path(r'^aac/department/create/$', views.CreateDepartment.as_view(), name='add-dept'),
    re_path(r'^aac/department/update/(?P<pk>\d+)/$', views.UpdateDepartment.as_view(), name='update-dept'),
    re_path(r'^aac/department/list/$', views.DepartmentList.as_view(), name='dept-list'),
    re_path(r'^aac/department/(?P<dept>\d+)/dp/create/$',views.CreateDegreeProgram.as_view(), name='add-dp'),
    re_path(r'^aac/department/(?P<dept>\d+)/dp/update/(?P<pk>\d+)/$',views.UpdateDegreeProgram.as_view(), name='update-dp'),
    re_path(r'^aac/department/(?P<dept>\d+)/dp/list/$', views.DegreeProgramList.as_view(),name='dp-list'),
    re_path(r'^aac/department/(?P<dept>\d+)/report/create/$',views.CreateReport.as_view(),name='add-rpt'),
    re_path(r'^aac/report/delete/(?P<pk>\d+)/$', views.DeleteReport.as_view(), name='delete-rpt'),
    re_path(r'^aac/report/list/$', views.ReportList.as_view(), name='report-list')
]