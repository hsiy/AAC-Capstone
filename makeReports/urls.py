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
    re_path(r'^report/list/search/$', views.ReportListSearchedDept.as_view(), name='search-reports-dept'),
    #Extra Report Entry URLs
    re_path(r'^report/(?P<report>\d+)/initial/$', views.ReportFirstPage.as_view(),name='rpt-first-page'),
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
    #Assesssment URLs
    re_path(r'^report/(?P<report>\d+)/assessment/summary/$', views.AssessmentSummary.as_view(), name='assessment-summary'),
    re_path(r'^report/(?P<report>\d+)/assessment/add/$', views.AddNewAssessment.as_view(), name='add-assessment'),  
    re_path(r'^report/(?P<report>\d+)/assessment/import/$', views.ImportAssessment_.as_view(), name='import-assessment'), 
    re_path(r'^report/(?P<report>\d+)/assessment/edit/new/(?P<assessIR>\d+)/$', views.EditNewAssessment_.as_view(), name='edit-new-assessment'),
    re_path(r'^report/(?P<report>\d+)/assessment/edit/impt/(?P<assessIR>\d+)/$', views.EditImportedAssessment_.as_view(), name='edit-impt-assessment'),
    re_path(r'^report/(?P<report>\d+)/assessment/supplements/(?P<assessIR>\d+)/$', views.SupplementUpload.as_view(), name='assessment-supplement'),
    re_path(r'^report/(?P<report>\d+)/assessment/supplements/import/(?P<assessIR>\d+)/$', views.ImportSupplement.as_view(), name='assessment-supplement-import'),
    re_path(r'^report/(?P<report>\d+)/assessment/comment/$', views.Section2Comment.as_view(),name='assessment-comment'),
    re_path(r'^report/(?P<report>\d+)/assessment/delete/new/(?P<pk>\d+)/$', views.DeleteNewAssessment.as_view(), name='delete-new-assessment'),
    re_path(r'^report/(?P<report>\d+)/assessment/delete/impt/(?P<pk>\d+)/$', views.DeleteImportedAssessment.as_view(), name='delete-impt-assessment'), 
    #AAC Admin URLS
    re_path(r'^aac/home/$', views.AdminHome.as_view(), name='admin-home'),
    re_path(r'^aac/college/create/$',views.CreateCollege.as_view(), name="add-college"),
    re_path(r'^aac/college/update/(?P<pk>\d+)/$', views.UpdateCollege.as_view(), name='update-college'),
    re_path(r'^aac/college/list/$', views.CollegeList.as_view(), name='college-list'),
    re_path(r'^aac/college/(?P<pk>\d+)/delete/$', views.DeleteCollege.as_view(), name='delete-college'),
    re_path(r'^aac/college/(?P<pk>\d+)/recover/$', views.RecoverCollege.as_view(), name='recover-college'),
    re_path(r'^aac/department/create/$', views.CreateDepartment.as_view(), name='add-dept'),
    re_path(r'^aac/department/update/(?P<pk>\d+)/$', views.UpdateDepartment.as_view(), name='update-dept'),
    re_path(r'^aac/department/list/$', views.DepartmentList.as_view(), name='dept-list'),
    re_path(r'^aac/department/(?P<pk>\d+)/delete/$', views.DeleteDepartment.as_view(), name='delete-dept'),
    re_path(r'^aac/department/(?P<pk>\d+)/recover/$', views.RecoverDepartment.as_view(), name='recover-dept'),
    re_path(r'^aac/department/(?P<dept>\d+)/dp/create/$',views.CreateDegreeProgram.as_view(), name='add-dp'),
    re_path(r'^aac/department/dp/update/(?P<pk>\d+)/$',views.UpdateDegreeProgram.as_view(), name='update-dp'),
    re_path(r'^aac/department/(?P<dept>\d+)/dp/list/$', views.DegreeProgramList.as_view(),name='dp-list'),
    re_path(r'^aac/department/dp/(?P<pk>\d+)/delete/$', views.DeleteDegreeProgram.as_view(), name='delete-dp'),
    re_path(r'^aac/department/dp/(?P<pk>\d+)/recover/$', views.RecoverDegreeProgram.as_view(), name='recover-dp'),
    re_path(r'^aac/department/(?P<dept>\d+)/report/create/$',views.CreateReport.as_view(),name='add-rpt'),
    re_path(r'^aac/report/delete/(?P<pk>\d+)/$', views.DeleteReport.as_view(), name='delete-rpt'),
    re_path(r'^aac/report/list/$', views.ReportList.as_view(), name='report-list'),
    re_path(r'^aac/report/list/searched/$', views.ReportListSearched.as_view(), name='search-reports'),
    re_path(r'^aac/account/create/$', views.MakeAccount.as_view(), name='make-account'),
    re_path(r'^aac/account/(?P<pk>\d+)/modify/$', views.ModifyAccount.as_view(), name='modify-account'),
    re_path(r'^aac/account/(?P<pk>\d+)/inactivate/$', views.InactivateUser.as_view(), name='inactivate-account'),
    re_path(r'^aac/report/success/$', views.GenerateReportSuccess.as_view(), name='gen-rpt-suc'),
    re_path(r'^aac/department/archived/list/$', views.ArchivedDepartments.as_view(), name='arc-depts'),
    re_path(r'^aac/college/archived/list/$', views.ArchivedColleges.as_view(), name='arc-colleges'),
    re_path(r'^aac/department/(?P<dept>)/dp/archived/list/$', views.ArchivedDegreePrograms.as_view(), name='arc-dps'),
    #Grading urls
    re_path(r'^aac/report/(?P<report>\d+)/grading/section1/$', views.Section1Grading.as_view(), name='grade-sec1'),
    re_path(r'^aac/report/(?P<report>\d+)/grading/review/$', views.RubricReview.as_view(), name='rub-review'),
    re_path(r'^aac/report/(?P<pk>\d+)/grading/return/$', views.ReturnReport.as_view(), name='ret-rept'),
    re_path(r'report/(?P<report>\d+)/feedback/$', views.Feedback.as_view(), name='rpt-feedback'),
    #Rubric urls
    re_path(r'^aac/rubric/list/$', views.RubricList.as_view(),name="rubric-list"),
    re_path(r'^aac/rubric/add/$', views.AddRubric.as_view(), name="add-rubric"),
    re_path(r'^aac/rubric/(?P<rubric>\d+)/addRI/$', views.AddRubricItems.as_view(), name='add-RI'),

    #Data Collection URLS
    re_path(r'^report/(?P<report>\d+)/datacollection/summary/$', views.DataCollectionSummary.as_view(), name='data-summary'),
    re_path(r'^report/(?P<report>\d+)/datacollection/assessment/(?P<assessment>\d+)/add/$', views.CreateDataCollectionRow.as_view(), name='add-data-collection'),
    re_path(r'^report/(?P<report>\d+)/datacollection/assessment/edit/(?P<dataCollection>\d+)/$', views.EditDataCollectionRow.as_view(), name='edit-data-collection'),
    re_path(r'^report/(?P<report>\d+)/datacollection/assessment/delete/(?P<pk>\d+)/$', views.DeleteDataCollectionRow.as_view(), name='delete-data-collection'),
    re_path(r'^report/(?P<report>\d+)/datacollection/assessment/(?P<assessment>\d+)/addsub/$', views.CreateSubassessmentRow.as_view(), name='add-subassessment'),
    re_path(r'^report/(?P<report>\d+)/datacollection/assessment/editsub/(?P<pk>\d+)/$', views.EditSubassessmentRow.as_view(), name='edit-subassessment'),
    re_path(r'^report/(?P<report>\d+)/datacollection/assessment/deletesub/(?P<pk>\d+)/$', views.DeleteSubassessmentRow.as_view(), name='delete-subassessment')
]