from django.urls import include, path, re_path
from django.conf.urls import url
from django.contrib import admin
from makeReports import views
from django.contrib.auth import views as auth_views
app_name = "makeReports"
urlpatterns = [
    #re_path(r'^$', views.IndexPage.as_view(), name="index"),
    #re_path(r'^showings/(?P<pk>\d+)/detail/$', views.ShowingDetail.as_view(), name="showing-detail"),
    re_path(r'^report/(?P<report>\d+)/slo/summary/$', views.SLOSummary.as_view(), name='slo-summary'),
    re_path(r'^report/(?P<report>\d+)/slo/add/$', views.AddNewSLO.as_view(), name='add-slo'),
    re_path(r'^report/(?P<report>\d+)/slo/import/$', views.ImportSLO.as_view(), name='import-slo'),
    re_path(r'^report/(?P<report>\d+)/slo/edit/new/(?P<sloIR>\d+)/$', views.EditNewSLO.as_view(), name='edit-new-slo'),
    re_path(r'^report/(?P<report>\d+)/slo/edit/impt/(?P<sloIR>\d+)/$', views.EditImportedSLO.as_view(), name='edit-impt-slo'),
    re_path(r'^report/(?P<report>\d+)/slo/stakeholders/$', views.StakeholderEntry.as_view(), name='slo-stakeholders')
]