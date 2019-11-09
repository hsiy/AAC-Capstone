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

        print(request.GET['decision'])
        dec = request.GET['decision']
        if dec == '1':
            #SLO: target vs actual


            # print('in decision 1')
            # dp = request.GET['report__degreeProgram']
            # print(dp)
            # vals = queryset.values('report__degreeProgram')
            # print(vals)
            # qDP = queryset.filter(report__degreeProgram=dp)
            # otherVals = qDP.values('sloIR__slo')
            # print(otherVals)
            # print(qDP)
            # s = request.GET['sloIR__slo']
            # print(s)
            # qSLO = qDP.filter(sloIR__slo=s)
            # print(qSLO)
            

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
                'Target': [],
                'Actual': []
            }
            index = []

            #targ = AssessmentVersion.objects.all()
            #actual = AssessmentData.objects.all()

            for year in range(bYear,eYear+1):
                qYear = queryset.filter(assessmentVersion__report__year=year)
                for assessA in qYear:
                    dataFrame['Target'].append(assessA.assessmentVersion.target)
                    dataFrame['Actual'].append(assessA.overallProficient/assessA.numberStudents)
                # s = queryset.values('sloIR__slo')
                # pkSLO = s.get('sloIR__slo')
                # print(s)
                # for t in targ:
                #     if t.slo == s.get('sloIR__slo'):
                #         dataFrame['Target'].append(t.target)
                # for a in actual:
                #     pkSLO = s.get('sloIR__slo')
                #     if a.assessmentVersion.slo == pkSLO:
                #         percent = a.overallProficient / a.numberStudents
                #         dataFrame['Actaul'].append(percent)
                index.append(year)

            
        elif dec == '2':
            #Number of SLOs met
            print('in decision 2')
            # filter_backends = (filters.DjangoFilterBackend,)
            # filterset_fields = {
            #     'report__degreeProgram':['exact'],
            #     'report__year':['gte','lte']
            # }
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
                'Met': [],
                'Partially Met': [],
                'Not Met': [],
                'Unknown': []
            }
            index = []

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
                index.append(year)
            
            df = pd.DataFrame(dataFrame, index=index)
            lines = df.plot.line()


        else:
            #Number of degree programs meeting target
            print('in decision 3')
            #queryset = SLOStatus.objects.all()
            # filter_backends = (filters.DjangoFilterBackend,)
            # filterset_fields = {
            #     'report__year':['gte','lte'],
            #     'report__degreeProgram__department':['exact']
            # }

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
            dataFrame = {}
            index = []
            
            ds = depQS.values('name')
            
            for d in ds.iterator():
                name = d.get('name')
                new = {name: []}
                dataFrame.update(new)

            for year in range(bYear,eYear+1):
                qYear = queryset.filter(report__year=year)
                for name in dataFrame:
                    qDP = qYear.filter(report__degreeProgram__name = str(name))
                    overall = qDP.count()
                    if overall != 0:
                        met = qDP.filter(status=SLO_STATUS_CHOICES[0][0]).count()
                        metP = met/overall
                    else:
                        metP = 0
                    dataFrame[name].append(metP)
                
                index.append(year)
            
            df = pd.DataFrame(dataFrame, index=index)
            lines = df.plot.line()

        return Response("hello")


