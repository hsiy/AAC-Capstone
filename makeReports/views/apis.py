"""
This file contains the JSON APIs used
"""
from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from makeReports.models import *
<<<<<<< HEAD
from makeReports.views.helperFunctions import text_processing
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
=======
import pandas as pd
>>>>>>> graphing

class DeptSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes departments to JSON with the primary key and name
    """
    class Meta:
        model = Department
        fields = ['pk','name']
class ProgSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes degree programs to JSON with the primary key, name, and level
    """
    class Meta:
        model = DegreeProgram
        fields = ['pk', 'name', 'level']
class SLOserializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes SLOs to JSON with the primary key and name
    """
    class Meta:
        model = SLOInReport
        fields = ['pk', 'goalText']
class DeptByColListAPI(generics.ListAPIView):
    """
    JSON API to gets active departments within specified college
    """
    queryset = Department.active_objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (['college'])
    serializer_class = DeptSerializer
class ProgByDeptListAPI(generics.ListAPIView):
    """
    JSON API to gets active degree programs within specified department
    """
    queryset = DegreeProgram.active_objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (['department'])
    serializer_class = ProgSerializer
class SloByDPListAPI(generics.ListAPIView):
    """
    JSON API to gets past slos within specified degree program
    """
    queryset = SLOInReport.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = {'report__degreeProgram':['exact'],
    'report__year':['gte','lte'],
    }
    serializer_class = SLOserializer

class SLOSuggestionsAPI(APIView):
    renderer_classes = [JSONRenderer]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        slo_text = request.data['slo_text']
        response = text_processing.create_suggestions_dict(slo_text)
        return(Response(response))
class createGraphAPI(views.APIView):
    """
    JSON API to get url of graph on file server with specified college,
    department, degree program, start and end dates, specific graph choice,
    and maybe slo to be graphed
    """
    def get(self,request,format=None):

        if 'decision' == 1:
            print('in decision 1')
            queryset = SLOStatus.objects.all()
            filter_backends = (filters.DjangoFilterBackend,)
            filterset_fields = {
                'report__degreeProgram':['exact'],
                'report__year':['gte','lte'],
                'slo':['exact']
            }
            
        elif 'decision' == 2:
            print('in decision 2')
            queryset = SLOStatus.objects.all()
            filter_backends = (filters.DjangoFilterBackend,)
            filterset_fields = {
                'report__degreeProgram':['exact'],
                'report__year':['gte','lte']
            }
            
            begYear=request.GET['report__year__gte']
            endYear = request.GET['report__year__lte']
            
            dataFrame = {
                'Met': [],
                'Partially Met': [],
                'Not Met': [],
                'Unknown': []
            }
            index = []

            for year in range(begYear,endYear+1):
                qYear = queryset.filter(report__year=year)
                overall = qYear.count()
                met = qYear.filter(status=SLO_STATUS_CHOICES[0][0]).count()
                partiallyMet = qYear.filter(status=SLO_STATUS_CHOICES[1][0]).count()
                notMet = qYear.filter(status=SLO_STATUS_CHOICES[2][0]).count()
                unknown = qYear.filter(status=SLO_STATUS_CHOICES[3][0]).count()
                metP = met/overall
                parP = partiallyMet/overall
                notP = notMet/overall
                unkP = unknown/overall
                dataFrame['Met'].append(metP)
                dataFrame['Partially Met'].append(parP)
                dataFrame['Not Met'].append(notP)
                dataFrame['Unknown'].append(unkP)
                index.append(year)
            
            df = pd.DataFrame(dataFrame, index=index)
            lines = df.plot.line()


            
        else:
            print('in decision 3')
            queryset = SLOStatus.objects.all()
            filter_backends = (filters.DjangoFilterBackend,)
            filterset_fields = {
                'report__year':['gte','lte'],
                'report__degreeProgram__department':['exact']
            }

            begYear=request.GET['report__year__gte']
            endYear = request.GET['report__year__lte']
            thisDep = request.GET['report__degreeProgram__department']

            dpQS = DegreeProgram.active_objects.all()
            depQS = dpQS.filter(department=thisDep)
            dataFrame = {}
            for dep in depQS:
                dataFrame.update(dep__name = [])
            index = []

            for year in range(begYear,endYear+1):
                qYear = queryset.filter(year=year)
                for i in range(len(dataFrame))
                    qDP = queryset.filter(report__degreeProgram__name = dataFrame[i])
                    overall = qDP.count()
                    met = qDP.filter(status=SLO_STATUS_CHOICES[0][0]).count()
                    metP = met/overall
                    dataFrame[i].append(metP)
                
                index.append(year)
            
            df = pd.DataFrame(dataFrame, index=index)
            lines = df.plot.line()

        return Response("hello")


