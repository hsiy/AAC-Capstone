"""
This file contains the JSON APIs used
"""
from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework import serializers
from makeReports.models import *


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
    Serializes slos to JSON with the primary key and name
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

class createGraphAPI(views.APIView):
    """
    JSON API to get url of graph on file server with specified college,
    department, degree program, start and end dates, specific graph choice,
    and maybe slo to be graphed
    """
    def get(self,request,format=None):
        queryset = SLOStatus.objects.all()

        if 'decision' == 1:
            print('in decision 1')
            filter_backends = (filters.DjangoFilterBackend,)
            filterset_fields = {
                'report__degreeProgram':['exact'],
                'report__year':['gte','lte'],
                'slo':['exact']
            }
            
        elif 'decision' == 2:
            print('in decision 2')
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
                qYear = queryset.filter(year=year)
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
            dataSource['chart'] = {
                "caption": "Number of Degree Programs Meeting Target"
            }
        return Response("hello")


