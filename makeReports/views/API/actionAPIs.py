"""
This file contains the APIs the front-end call to trigger an action on the back-end
"""
from rest_framework import generics
from rest_framework import views, status
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from makeReports.models import *
from makeReports.choices import *
from makeReports.views.helperFunctions import text_processing
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta

class ClearOverrideAPI(APIView):
    """
    Clears the overriden aggregates and SLO statuses
    """
    renderer_classes = [JSONRenderer]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        """
        Clears the overridden aggregates and SLO statuses for given report

        Args:
            request (HttpRequest): the request to the API
            format (None): not used
        Returns:
            response (Response): empty response

        Notes:
            Expects primary key of report to be passed in GET request as 'pk'
        """
        pk = int(request.query_params['pk'])
        rpt = Report.objects.get(pk=pk)
        if((rpt.degreeProgram.department==request.user.profile.department) or request.user.profile.aac):
            #only proceed if the person truly has the right to modify the report
            statuses = SLOStatus.objects.filter(sloIR__report__pk=pk, override=True)
            for status in statuses:
                status.override = False
                status.save()
                update_status(status,0,0, status.sloIR)
            aggs = AssessmentAggregate.objects.filter(assessmentVersion__report__pk=pk, override=True)
            for agg in aggs:
                agg.override = False
                agg.save()
                update_agg(agg,0,0,agg.assessmentVersion)
            return Response()

