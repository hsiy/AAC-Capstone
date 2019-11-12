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
from makeReports.choices import *
from makeReports.views.helperFunctions import text_processing
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
import tempfile
import django.core.files as files
import matplotlib.pyplot as plt
import io
from datetime import datetime, timedelta
from matplotlib.ticker import FuncFormatter

import pandas as pd


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
class FileSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes SLOs to JSON with the primary key and name
    """
    class Meta:
        model = Graph
        fields = "__all__"
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
        #Start by deleting some old graphs
        graphs = Graph.objects.filter(dateTime__date__lte=datetime.now()-timedelta(minutes=20))
        for g in graphs:
            g.graph.delete(save=False)
            g.delete()
        dec = request.GET['decision']
        if dec == '1':
            #specific SLO
            begYear=request.GET['report__year__gte']
            endYear = request.GET['report__year__lte']
            bYear=int(begYear)
            eYear=int(endYear)
            degreeProgram = request.GET['report__degreeProgram']
            slo = request.GET['sloIR']
            queryset = AssessmentAggregate.objects.filter(
                assessmentVersion__report__year__gte=begYear,
                assessmentVersion__report__year__lte = endYear,
                assessmentVersion__report__degreeProgram__pk = degreeProgram,
                assessmentVersion__slo__pk = slo
                )

            dataFrame = {
                'Year': [],
                'Target': [],
                'Actual': []
            }
            index = []


            for year in range(bYear,eYear+1):
                qYear = queryset.filter(assessmentVersion__report__year=year)
                for assessA in qYear:
                    dataFrame['Year'].append(year)
                    dataFrame['Target'].append(assessA.assessmentVersion.target)
                    dataFrame['Actual'].append(assessA.aggregate_proficiency)
                
                index.append(year)
            df = pd.DataFrame(data=dataFrame)
            #lines = df.plot.line()
            lines = df.plot(kind='bar',x='Year',y=['Target','Actual'])
            lines.set(xlabel="Year", ylabel="Percentage")
            figure = lines.get_figure()
            
            
            
        elif dec == '2':
            #Number of SLOs met

           
            begYear=request.GET['report__year__gte']
            endYear = request.GET['report__year__lte']
            bYear=int(begYear)
            eYear=int(endYear)
            degreeProgram = request.GET['report__degreeProgram']
            queryset = SLOStatus.objects.filter(
                report__year__gte = begYear,
                report__year__lte = endYear,
                report__degreeProgram__pk = degreeProgram
                )
            
            dataFrame = {
                'Year':[],
                'Met': [],
                'Partially Met': [],
                'Not Met': [],
                'Unknown': []
            }

            for year in range(bYear,eYear+1):
                qYear = queryset.filter(report__year=year)
                overall = qYear.count()
                if overall != 0:
                    met = qYear.filter(status=SLO_STATUS_CHOICES[0][0]).count()
                    partiallyMet = qYear.filter(status=SLO_STATUS_CHOICES[1][0]).count()
                    notMet = qYear.filter(status=SLO_STATUS_CHOICES[2][0]).count()
                    unknown = qYear.filter(status=SLO_STATUS_CHOICES[3][0]).count()
                    metP = met/overall
                    parP = partiallyMet/overall
                    notP = notMet/overall
                    unkP = unknown/overall
                else:
                    metP = 0
                    parP = 0
                    notP = 0
                    unkP = 0
                dataFrame['Met'].append(metP)
                dataFrame['Partially Met'].append(parP)
                dataFrame['Not Met'].append(notP)
                dataFrame['Unknown'].append(unkP)
                dataFrame['Year'].append(year)
            
            df = pd.DataFrame(dataFrame)
            lines = df.plot(kind='bar',x='Year',y=['Met','Partially Met','Not Met','Unknown'])
            lines.set(xlabel="Year", ylabel="Percentage")
            #lines = df.plot(kind='line',x='Year',y='Partially Met',ax=ax)
            #lines = df.plot(kind='line',x='Year',y='Not Met',ax=ax)
            #lines = df.plot(kind='line',x='Year',y='Unknown',ax=ax)
            figure = lines.get_figure()
            


        else:
            #Number of degree programs meeting target

            begYear=request.GET['report__year__gte']
            endYear = request.GET['report__year__lte']
            bYear=int(begYear)
            eYear=int(endYear)
            thisDep = request.GET['report__degreeProgram__department']
            queryset = SLOStatus.objects.filter(
                report__year__gte=begYear,
                report__year__lte = endYear,
                report__degreeProgram__department__pk = thisDep
                )
            #dpQS = DegreeProgram.active_objects.all()
            depQS = DegreeProgram.active_objects.filter(department=thisDep)
            dataFrame = {
                'Year':[]
            }
            index = []
            
            ds = depQS.values('name')
            
            for d in ds.iterator():
                name = d.get('name')
                new = {name: []}
                dataFrame.update(new)

            for year in range(bYear,eYear+1):
                qYear = queryset.filter(report__year=year)
                for name in dataFrame.keys():
                    if name is not "Year":
                        qDP = qYear.filter(report__degreeProgram__name = str(name))
                        overall = qDP.count()
                        if overall != 0:
                            met = qDP.filter(status=SLO_STATUS_CHOICES[0][0]).count()
                            metP = met/overall
                        else:
                            metP = 0
                        dataFrame[name].append(metP)
                dataFrame['Year'].append(year)
            df = pd.DataFrame(dataFrame)
            yVals = list(dataFrame.keys()).remove('Year')
            lines = df.plot(kind='bar',x='Year',y=yVals)
            lines.set(xlabel="Year", ylabel="Percentage")
            lines.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y))) 
            figure = lines.get_figure()
        #f1 = tempfile.TemporaryFile()
        #figure.savefig(f1)
        #f2 = files.File(f1)
        f1 = io.BytesIO()
        figure.savefig(f1, format="png", bbox_inches='tight')
        content_file = files.images.ImageFile(f1)
        graphObj = Graph.objects.create(dateTime=datetime.now())
        graphObj.graph.save("graph-"+str(request.user)+"-"+str(datetime.now())+".png",content_file)
        return Response(graphObj.graph.url)


