from django.urls import include, path, re_path
from django.conf.urls import url
from django.contrib import admin
from makeReports import views
from django.contrib.auth import views as auth_views
app_name = "makeReports"
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.HomePage.as_view(), name="home-page"),
    re_path(r'^report/list/$', views.FacultyReportList.as_view(), name='rpt-list-dept'),
    #SLO Urls
    re_path(r'^report/(?P<report>\d+)/slo/summary/$', views.SLOSummary.as_view(), name='slo-summary'),
    re_path(r'^report/(?P<report>\d+)/slo/add/$', views.AddNewSLO.as_view(), name='add-slo'),
    re_path(r'^report/(?P<report>\d+)/slo/import/$', views.ImportSLO.as_view(), name='import-slo'),
    re_path(r'^report/(?P<report>\d+)/slo/edit/new/(?P<sloIR>\d+)/$', views.EditNewSLO.as_view(), name='edit-new-slo'),
    re_path(r'^report/(?P<report>\d+)/slo/edit/impt/(?P<sloIR>\d+)/$', views.EditImportedSLO.as_view(), name='edit-impt-slo'),
    re_path(r'^report/(?P<report>\d+)/slo/stakeholders/$', views.StakeholderEntry.as_view(), name='slo-stakeholders'),
    re_path(r'^report/(?P<report>\d+)/slo/stakeholders/import/$', views.ImportStakeholderEntry.as_view(), name='slo-stk-import'),
    re_path(r'^report/(?P<report>\d+)/slo/comment/$', views.Section1Comment.as_view(),name='slo-comment'),
    re_path(r'^report/(?P<report>\d+)/slo/delete/new/(?P<pk>\d+)/$', views.DeleteNewSLO.as_view(), name='delete-new-slo'),
    re_path(r'^report/(?P<report>\d+)/slo/delete/impt/(?P<pk>\d+)/$', views.DeleteImportedSLO.as_view(), name='delete-impt-slo'),    
    #AAC Admin URLS
    re_path(r'^aac/home/$', views.AdminHome.as_view(), name='admin-home'),
    re_path(r'^aac/college/create/$',views.CreateCollege.as_view(), name="add-college"),
    re_path(r'^aac/college/update/(?P<pk>\d+)/$', views.UpdateCollege.as_view(), name='update-college'),
    re_path(r'^aac/college/list/$', views.CollegeList.as_view(), name='college-list'),
    re_path(r'^aac/college/(?P<pk>\d+)/delete/$', views.DeleteCollege.as_view(), name='delete-college'),
    re_path(r'^aac/department/create/$', views.CreateDepartment.as_view(), name='add-dept'),
    re_path(r'^aac/department/update/(?P<pk>\d+)/$', views.UpdateDepartment.as_view(), name='update-dept'),
    re_path(r'^aac/department/list/$', views.DepartmentList.as_view(), name='dept-list'),
    re_path(r'^aac/department/(?P<pk>\d+)/delete/$', views.DeleteDepartment.as_view(), name='delete-dept'),
    re_path(r'^aac/department/(?P<dept>\d+)/dp/create/$',views.CreateDegreeProgram.as_view(), name='add-dp'),
    re_path(r'^aac/department/dp/update/(?P<pk>\d+)/$',views.UpdateDegreeProgram.as_view(), name='update-dp'),
    re_path(r'^aac/department/(?P<dept>\d+)/dp/list/$', views.DegreeProgramList.as_view(),name='dp-list'),
    re_path(r'^aac/department/dp/(?P<pk>\d+)/delete/$', views.DeleteDegreeProgram.as_view(), name='delete-dp'),
    re_path(r'^aac/department/(?P<dept>\d+)/report/create/$',views.CreateReport.as_view(),name='add-rpt'),
    re_path(r'^aac/report/delete/(?P<pk>\d+)/$', views.DeleteReport.as_view(), name='delete-rpt'),
    re_path(r'^aac/report/list/$', views.ReportList.as_view(), name='report-list'),
    re_path(r'^aac/account/create/$', views.MakeAccount.as_view(), name='make-account'),
    re_path(r'^aac/report/success/$', views.GenerateReportSuccess.as_view(), name='gen-rpt-suc'),
    #Grading urls
    re_path(r'^aac/report/(?P<report>\d+)/grading/section1/$', views.Section1Grading.as_view(), name='grade-sec1'),
    #Rubric urls
    re_path(r'^aac/rubric/list/$', views.RubricList.as_view(),name="rubric-list"),
    re_path(r'^aac/rubric/add/$', views.AddRubric.as_view(), name="add-rubric"),
    re_path(r'^aac/rubric/(?P<rubric>\d+)/addRI/$', views.AddRubricItems.as_view(), name='add-RI')


]