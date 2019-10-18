from django.urls import include, path, re_path
from makeReports import views

app_name = "makeReports"
urlpatterns = [
    path('summernote/', include('django_summernote.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.HomePage.as_view(), name="home-page"),
    path('help/',views.HelpPage.as_view(),name='help-page'),
    re_path(r'^user/modify/$', views.UserModifyAccount.as_view(),name='modify-acct'),
    re_path(r'^report/list/$', views.FacultyReportList.as_view(), name='rpt-list-dept'),
    re_path(r'^report/list/search/$', views.ReportListSearchedDept.as_view(), name='search-reports-dept'),
    re_path(r'^report/(?P<pk>\d+)/view/$', views.DisplayReport.as_view(),name='view-rpt'),
    #Extra Report Entry URLs
    re_path(r'^report/(?P<pk>\d+)/initial/$', views.ReportFirstPage.as_view(),name='rpt-first-page'),
    re_path(r'^report/(?P<report>\d+)/supplements/list/$', views.FinalReportSupplements.as_view(),name='rpt-sup-list'),
    re_path(r'^report/(?P<report>\d+)/supplement/add/$', views.AddEndSupplements.as_view(),name='add-rpt-sup'),
    re_path(r'^report/(?P<report>\d+)/supplement/(?P<pk>\d+)/delete/$', views.DeleteEndSupplements.as_view(),name='delete-rpt-sup'),
    re_path(r'^report/(?P<report>\d+)/submit/$', views.SubmitReport.as_view(),name='submit-report'),
    re_path(r'^report/submit/success/$', views.SuccessSubmit.as_view(),name='sub-suc'),
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
    re_path(r'^report/(?P<report>\d+)/slo/(?P<slo>\d+)/assessment/add/$', views.AddNewAssessmentSLO.as_view(), name='add-assessment-slo'),  
    re_path(r'^report/(?P<report>\d+)/assessment/import/$', views.ImportAssessment.as_view(), name='import-assessment'), 
    re_path(r'^report/(?P<report>\d+)/slo/(?P<slo>\d+)/assessment/import/$', views.ImportAssessmentSLO.as_view(), name='import-assessment-slo'), 
    re_path(r'^report/(?P<report>\d+)/assessment/edit/new/(?P<assessIR>\d+)/$', views.EditNewAssessment.as_view(), name='edit-new-assessment'),
    re_path(r'^report/(?P<report>\d+)/assessment/edit/impt/(?P<assessIR>\d+)/$', views.EditImportedAssessment.as_view(), name='edit-impt-assessment'),
    re_path(r'^report/(?P<report>\d+)/assessment/supplements/upload/(?P<assessIR>\d+)/$', views.SupplementUpload.as_view(), name='assessment-supplement-upload'),
    re_path(r'^report/(?P<report>\d+)/assessment/supplements/import/(?P<assessIR>\d+)/$', views.ImportSupplement.as_view(), name='assessment-supplement-import'),
    re_path(r'^report/(?P<report>\d+)/assessment/supplements/delete/(?P<assessIR>\d+)/(?P<pk>\d+)/$', views.DeleteSupplement.as_view(), name='delete-supplement'),
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
    re_path(r'^aac/department/(?P<dept>\d+)/dp/update/(?P<pk>\d+)/$',views.UpdateDegreeProgram.as_view(), name='update-dp'),
    re_path(r'^aac/department/(?P<dept>\d+)/dp/list/$', views.DegreeProgramList.as_view(),name='dp-list'),
    re_path(r'^aac/department/(?P<dept>\d+)/dp/(?P<pk>\d+)/delete/$', views.DeleteDegreeProgram.as_view(), name='delete-dp'),
    re_path(r'^aac/department/(?P<dept>\d+)/dp/(?P<pk>\d+)/recover/$', views.RecoverDegreeProgram.as_view(), name='recover-dp'),
    re_path(r'^aac/department/(?P<dept>\d+)/report/create/$',views.CreateReport.as_view(),name='add-rpt'),
    re_path(r'^aac/dp/(?P<dP>\d+)/report/create/$',views.CreateReportByDP.as_view(),name='add-rpt-dp'),
    re_path(r'^aac/report/delete/(?P<pk>\d+)/$', views.DeleteReport.as_view(), name='delete-rpt'),
    re_path(r'^aac/report/submit/(?P<pk>\d+)/$', views.ManualReportSubmit.as_view(), name='manual-submit-rpt'),
    re_path(r'^aac/report/list/$', views.ReportList.as_view(), name='report-list'),
    re_path(r'^aac/report/list/searched/$', views.ReportListSearched.as_view(), name='search-reports'),
    re_path(r'^aac/account/create/$', views.MakeAccount.as_view(), name='make-account'),
    re_path(r'^aac/account/list/$', views.AccountList.as_view(), name='account-list'),
    re_path(r'^aac/account/list/search/$', views.SearchAccountList.as_view(), name='search-account-list'),
    re_path(r'^aac/account/(?P<pk>\d+)/modify/$', views.ModifyAccount.as_view(), name='aac-modify-account'),
    re_path(r'^aac/account/(?P<pk>\d+)/inactivate/$', views.InactivateUser.as_view(), name='inactivate-account'),
    re_path(r'^aac/report/success/$', views.GenerateReportSuccess.as_view(), name='gen-rpt-suc'),
    re_path(r'^aac/department/archived/list/$', views.ArchivedDepartments.as_view(), name='arc-depts'),
    re_path(r'^aac/college/archived/list/$', views.ArchivedColleges.as_view(), name='arc-colleges'),
    re_path(r'^aac/department/(?P<dept>\d+)/dp/archived/list/$', views.ArchivedDegreePrograms.as_view(), name='arc-dps'),
    re_path(r'^aac/gg/list/$', views.ListActiveGradGoals.as_view(),name='gg-list'),
    re_path(r'^aac/gg/list/inactive/$', views.ListInactiveGradGoals.as_view(),name='old-gg-list'),
    re_path(r'^aac/gg/(?P<pk>\d+)/update/$', views.UpdateGradGoal.as_view(),name='update-gg'),
    re_path(r'^aac/gg/add/$', views.MakeGradGoal.as_view(),name='add-gg'),
    re_path(r'^aac/ann/list/$', views.ListAnnouncements.as_view(),name='announ-list'),
    re_path(r'^aac/ann/add/$', views.MakeAnnouncement.as_view(),name='add-announ'),
    re_path(r'^aac/ann/(?P<pk>\d+)/delete/$', views.DeleteAnnouncement.as_view(),name='delete-announ'),
    re_path(r'^aac/ann/(?P<pk>\d+)/modify/$', views.ModifyAnnouncement.as_view(),name='edit-announ'),

    #Grading urls
    re_path(r'^aac/report/(?P<report>\d+)/grading/section1/$', views.Section1Grading.as_view(), name='grade-sec1'),
    re_path(r'^aac/report/(?P<report>\d+)/grading/section2/$', views.Section2Grading.as_view(), name='grade-sec2'),
    re_path(r'^aac/report/(?P<report>\d+)/grading/section3/$', views.Section3Grading.as_view(), name='grade-sec3'),
    re_path(r'^aac/report/(?P<report>\d+)/grading/section4/$', views.Section4Grading.as_view(), name='grade-sec4'),
    re_path(r'^aac/report/(?P<report>\d+)/grading/comment/$', views.OverallComment.as_view(), name='grade-comment'),
    re_path(r'^aac/report/(?P<report>\d+)/grading/review/$', views.RubricReview.as_view(), name='rub-review'),
    re_path(r'^aac/report/(?P<pk>\d+)/grading/return/$', views.ReturnReport.as_view(), name='ret-rept'),
    re_path(r'report/(?P<report>\d+)/feedback/$', views.Feedback.as_view(), name='rpt-feedback'),
    #Rubric urls
    re_path(r'^aac/rubric/list/$', views.RubricList.as_view(),name="rubric-list"),
    re_path(r'^aac/rubric/list/searched/$', views.SearchRubricList.as_view(),name="search-rubric-list"),
    re_path(r'^aac/rubric/add/$', views.AddRubric.as_view(), name="add-rubric"),
    re_path(r'^aac/rubric/(?P<rubric>\d+)/addRI/$', views.AddRubricItems.as_view(), name='add-RI'),
    re_path(r'^aac/rubric/(?P<pk>\d+)/view/$', views.ViewRubric.as_view(), name='view-rubric'),
    re_path(r'^aac/rubric/(?P<pk>\d+)/update/$', views.UpdateRubricFile.as_view(), name='update-rubric'),
    re_path(r'^aac/rubric/(?P<pk>\d+)/delete/$', views.DeleteRubric.as_view(), name='delete-rubric'),
    re_path(r'^aac/rubric/(?P<rubric>\d+)/item/(?P<pk>\d+)/edit/$', views.UpdateRubricItem.as_view(), name='update-RI'),
    re_path(r'^aac/rubric/(?P<rubric>\d+)/duplicate/$', views.DuplicateRubric.as_view(), name='dup-rub'),
    re_path(r'^aac/rubric/(?P<rubric>\d+)/item/(?P<pk>\d+)/delete/$', views.DeleteRubricItem.as_view(), name='delete-RI'),
    #Data Collection URLS
    re_path(r'^report/(?P<report>\d+)/datacollection/summary/$', views.DataCollectionSummary.as_view(), name='data-summary'),
    re_path(r'^report/(?P<report>\d+)/datacollection/assessment/(?P<assessment>\d+)/add/$', views.CreateDataCollectionRow.as_view(), name='add-data-collection'),
    re_path(r'^report/(?P<report>\d+)/datacollection/assessment/(?P<assessment>\d+)/add/assess/$', views.CreateDataCollectionRowAssess.as_view(), name='add-data-collection-assess'),
    re_path(r'^report/(?P<report>\d+)/datacollection/assessment/edit/(?P<dataCollection>\d+)/$', views.EditDataCollectionRow.as_view(), name='edit-data-collection'),
    re_path(r'^report/(?P<report>\d+)/datacollection/assessment/delete/(?P<pk>\d+)/$', views.DeleteDataCollectionRow.as_view(), name='delete-data-collection'),
    re_path(r'^report/(?P<report>\d+)/datacollection/assessment/(?P<assessment>\d+)/addsub/$', views.CreateSubassessmentRow.as_view(), name='add-subassessment'),
    re_path(r'^report/(?P<report>\d+)/datacollection/assessment/editsub/(?P<pk>\d+)/$', views.EditSubassessmentRow.as_view(), name='edit-subassessment'),
    re_path(r'^report/(?P<report>\d+)/datacollection/assessment/deletesub/(?P<pk>\d+)/$', views.DeleteSubassessmentRow.as_view(), name='delete-subassessment'),
    re_path(r'^report/(?P<report>\d+)/datacollection/slostatus/(?P<slopk>\d+)/$', views.NewSLOStatus.as_view(), name='add-slo-status'),
    re_path(r'^report/(?P<report>\d+)/datacollection/slostatus/(?P<slopk>\d+)/(?P<statuspk>\d+)/$', views.EditSLOStatus.as_view(), name='edit-slo-status'),
    re_path(r'^report/(?P<report>\d+)/datacollection/resultcommunication/$', views.NewResultCommunication.as_view(), name='add-result-communication'),
    re_path(r'^report/(?P<report>\d+)/datacollection/resultcommunication/(?P<resultpk>\d+)/$', views.EditResultCommunication.as_view(), name='edit-result-communication'),
    re_path(r'^report/(?P<report>\d+)/datacollection/comment/$',views.Section3Comment.as_view(),name='data-comment'),
    re_path(r'^report/(?P<report>\d+)/datacollection/supplement/create/$',views.DataAssessmentAddInfo.as_view(),name='add-data-sup'),
    re_path(r'^report/(?P<report>\d+)/datacollection/supplement/(?P<pk>\d+)/edit/$',views.DataAssessmentUpdateInfo.as_view(),name='update-data-sup'),
    re_path(r'^report/(?P<report>\d+)/datacollection/supplement/(?P<pk>\d+)/delete/$',views.DataAssessmentDeleteInfo.as_view(),name='delete-data-sup'),
    #Decisions and Actions URLs
    re_path(r'^report/(?P<report>\d+)/decisionsactions/$', views.DecisionsActionsSummary.as_view(), name='decisions-actions-summary'),
    re_path(r'^report/(?P<report>\d+)/decisionsactions/(?P<slopk>\d+)/$', views.AddDecisionAction.as_view(), name='add-decisions-actions'),
    re_path(r'^report/(?P<report>\d+)/decisionsactions/(?P<slopk>\d+)/slo/$', views.AddDecisionActionSLO.as_view(), name='add-decisions-actions-slo'),
    re_path(r'^report/(?P<report>\d+)/decisionsactions/(?P<slopk>\d+)/(?P<pk>\d+)/$', views.EditDecisionAction.as_view(), name='edit-decisions-actions'),
    re_path(r'^report/(?P<report>\d+)/decisionsactions/(?P<slopk>\d+)/(?P<pk>\d+)/slo/$', views.EditDecisionActionSLO.as_view(), name='edit-decisions-actions-slo'),
    re_path(r'^report/(?P<report>\d+)/decisionsactions/(?P<slopk>\d+)/redirect/$', views.AddEditRedirect.as_view(), name='add-edit-redirect'),
    re_path(r'^report/(?P<report>\d+)/decisionsactions/comment/$',views.Section4Comment.as_view(),name='d-a-comment'),
    #PDF Generators
    re_path(r'^pdf/report/(?P<report>\d+)/rubric/graded/$',views.GradedRubricPDFGen.as_view(), name='graded-rub-pdf'),
    re_path(r'^pdf/report/(?P<report>\d+)/nosups/$', views.ReportPDFGen.as_view(), name='report-pdf-no-sups'),
    re_path(r'^pdf/report/(?P<report>\d+)/sups/$', views.reportPDF,name='report-pdf'),
    re_path(r'^pdf/report/(?P<report>\d+)/sups/view/$', views.PDFViewer.as_view(),name='trying-to-fix'),
    re_path(r'^pdf/rubric/(?P<rubric>\d+)/auto/$', views.UngradedRubric,name='rubric-auto-pdf'),
]