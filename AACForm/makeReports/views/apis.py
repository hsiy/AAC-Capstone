"""
This file contains the JSON APIs used
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
class SLOParentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes :class:`~makeReports.models.SLO` into just its primary key
    """
    class Meta:
        model = SLO
        fields = ['pk']
class SLOSerializerWithParent(serializers.HyperlinkedModelSerializer):
    """
    Serializes SLOs (:class:`~makeReports.models.SLOInReport`) to JSON with the primary key and name and primary key of SLO
    """
    slo = SLOParentSerializer()
    class Meta:
        model = SLOInReport
        fields = ['pk', 'goalText','slo']
class AssessmentParentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes parent assessments (:class:`~makeReports.models.Assessment`) into its primary key and title
    """
    class Meta:
        model = Assessment
        fields = ['pk','title']
class Assessmentserializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes assessments (:class:`~makeReports.models.AssessmentVersion`) to JSON with the primary key and and title
    """
    assessment =AssessmentParentSerializer()
    class Meta:
        model = SLOInReport
        fields = ['pk', 'assessment']
class FileSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes graphs to JSON with all fields 
    """
    class Meta:
        model = Graph
        fields = "__all__"
class DeptByColListAPI(generics.ListAPIView):
    """
    JSON API to gets active departments within specified college

    Notes:
        'college' is GET parameter to filter college primary key
    """
    queryset = Department.active_objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (['college'])
    serializer_class = DeptSerializer
class ProgByDeptListAPI(generics.ListAPIView):
    """
    JSON API to gets active degree programs within specified department

    Notes:
        'department' is GET parameter to filter by department primary key
    """
    queryset = DegreeProgram.active_objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (['department'])
    serializer_class = ProgSerializer
class SloByDPListAPI(generics.ListAPIView):
    """
    JSON API to gets past SLOs :class:`~makeReports.models.SLO` within specified degree program
    
    Notes:
        'report__degreeProgram' (degreeProgram primary key), 'report__year__gte' (min year),
        'report__year__lte' (max year) are the GET request parameters
    """
    queryset = SLOInReport.objects.all()
    #Gets the most recent SLOInReport for each SLO
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = {'report__degreeProgram':['exact'],
    'report__year':['gte','lte'],
    }
    serializer_class = SLOSerializerWithParent
    def get_queryset(self):
        """
        Gets the filtered queryset, and picks the most recent SLOInReport for each parent SLO

        Returns:
            QuerySet : queryset of SLOs that match parameters
        Notes:
            .order_by(...).distinct(...) is only supported by PostgreSQL
        """
        qS = super(SloByDPListAPI,self).get_queryset()
        qS = qS.order_by('slo','-report__year').distinct('slo')
        return qS
class AssessmentBySLO(generics.ListAPIView):
    """
    Filters AssessmentVersion to get the most recent assessment version for each parent assessment

    Notes:
        'slo__slo' (parent SLO pk), 'report__year__gte' (min year), 'report__year__lte' (max year)
        are the GET parameters
    """
    #queryset = AssessmentVersion.objects.order_by('assessment','-report__year').distinct('assessment')
    queryset = AssessmentVersion.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = {
        'slo__slo':['exact'],
        'report__year':['gte','lte'],
    }
    serializer_class = Assessmentserializer
    #filterset_class = AssessmentSLOFilterClass
    def get_queryset(self):
        """
        Gets the filtered queryset, and picks the most recent AssessmentVersion for each parent Assessment

        Returns:
            QuerySet : queryset of assessments that match parameters
        Notes:
            .order_by(...).distinct(...) is only supported by PostgreSQL
        """
        qS = super(AssessmentBySLO,self).get_queryset()
        qS = qS.order_by('assessment','-report__year').distinct('assessment')
        return qS

class SLOSuggestionsAPI(APIView):
    """
    Generates suggestions for SLOs based upon goal text
    """
    renderer_classes = [JSONRenderer]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        """
        When API is posted to return dictonary of suggestions

        Returns:
            dict : dictionary of suggestions relating to SLO
        """
        slo_text = request.data['slo_text']
        response = text_processing.create_suggestions_dict(slo_text)
        return(Response(response))
class BloomsSuggestionsAPI(APIView):
    """
    Returns suggested words based upon Bloom's level
    """
    renderer_classes = [JSONRenderer]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        """
        When API is posted to return dictonary of suggestions

        Returns:
            dict : dictionary of suggestions relating to SLO
        """
        level = request.data['level']
        response = text_processing.blooms_words(level)
        return(Response(response))
def get_specificSLO_graph(request):
    """
    Graphs a specific SLO/Assessment combo performance over time

    Args:
        request (HttpRequest): contains GET parameters
    Returns:
        matplotlib.figure.Figure : figure, i.e. the graph
    Notes:
        Uses POST data 'report__year__gte' (min year), 'report__year__lte' (max year),
        'report__degreeProgram' (degree program pk), 'sloIR' (SLOInReport primary key),
        'assess' (Assessment primary key)
    """
    begYear=request.data['report__year__gte']
    endYear = request.data['report__year__lte']
    bYear=int(begYear)
    eYear=int(endYear)
    degreeProgram = request.data['report__degreeProgram']
    slo = request.data['sloIR']
    sloObj = SLOInReport.objects.get(pk=slo)
    assess = request.data['assess']
    queryset = AssessmentAggregate.objects.filter(
        assessmentVersion__assessment__pk = assess,
        assessmentVersion__report__year__gte=begYear,
        assessmentVersion__report__year__lte = endYear,
        assessmentVersion__report__degreeProgram__pk = degreeProgram,
        assessmentVersion__slo__slo = sloObj.slo
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
            dataFrame['Target'].append(assessA.assessmentVersion.target/100)
            dataFrame['Actual'].append(assessA.aggregate_proficiency/100)
        index.append(year)
    df = pd.DataFrame(data=dataFrame)
    #lines = df.plot.line()
    lines = df.plot(kind='bar',x='Year',y=['Target','Actual'])
    lines.set(xlabel="Year", ylabel="Percentage")
    lines.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y))) 
    figure = lines.get_figure()
    return figure
def get_numberSLOs_graph(request):
    """
    Generate the figure that graphs number of each SLO status within a degree program

    Args:
        request (HttpRequest): contains the GET parameters
    Returns:
        matplotlib.figure.Figure : figure, i.e. the graph
    Notes:
        Uses POST parameters 'report__year__gte' (min year), 'report__year__lte' (max year),
        'report__degreeProgram' (degree program pk), and sloWeights (weights of SLOs)
    """
    begYear=request.data['report__year__gte']
    endYear = request.data['report__year__lte']
    sloWeights = request.data['sloWeights']
    bYear=int(begYear)
    eYear=int(endYear)
    degreeProgram = request.data['report__degreeProgram']
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
            met = 0
            partiallyMet = 0
            notMet = 0
            unknown = 0
            for weightPk in sloWeights.keys():
                met += qYear.filter(
                    status=SLO_STATUS_CHOICES[0][0],
                    SLO__pk=weightPk).count()*int(sloWeights[weightPk])
                partiallyMet += qYear.filter(
                    status=SLO_STATUS_CHOICES[1][0],
                    SLO__pk=weightPk).count()*int(sloWeights[weightPk])
                notMet += qYear.filter(
                    status=SLO_STATUS_CHOICES[2][0],
                    SLO__pk=weightPk).count()*int(sloWeights[weightPk])
                unknown += qYear.filter(
                    status=SLO_STATUS_CHOICES[3][0],
                    SLO__pk=weightPk).count()*int(sloWeights[weightPk])
            # met = qYear.filter(status=SLO_STATUS_CHOICES[0][0]).count()
            # partiallyMet = qYear.filter(status=SLO_STATUS_CHOICES[1][0]).count()
            # notMet = qYear.filter(status=SLO_STATUS_CHOICES[2][0]).count()
            # unknown = qYear.filter(status=SLO_STATUS_CHOICES[3][0]).count()
            sumWithWeights = met+partiallyMet+notMet+unknown
            metP = met/sumWithWeights
            parP = partiallyMet/sumWithWeights
            notP = notMet/sumWithWeights
            unkP = unknown/sumWithWeights
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
    lines.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y))) 
    #lines = df.plot(kind='line',x='Year',y='Partially Met',ax=ax)
    #lines = df.plot(kind='line',x='Year',y='Not Met',ax=ax)
    #lines = df.plot(kind='line',x='Year',y='Unknown',ax=ax)
    figure = lines.get_figure()
    return figure
def get_degreeProgramSuccess_graph(request):
    """
    Generates graph of percentage of SLOs being met by degree programs within department

    Returns:
        matplotlib.figure.Figure : figure, i.e. the graph
    Notes:
        Uses POST data 'report__year__gte' (min year), 'report__year__lte' (max year),
        'report__degreeProgram__department' (department pk)
    """
    begYear = request.data['report__year__gte']
    endYear = request.data['report__year__lte']
    bYear=int(begYear)
    eYear=int(endYear)
    thisDep = request.data['report__degreeProgram__department']
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
    
    # ds = depQS.values('name')
    
    # for d in ds.iterator():
    #     name = d.get('name')+" ("+d.get('level')+")"
    #     new = {name: []}
    #     dataFrame.update(new)

    for year in range(bYear,eYear+1):
        qYear = queryset.filter(report__year=year)
        for d in depQS:
            qDP = qYear.filter(report__degreeProgram = d)
            overall = qDP.count()
            if overall != 0:
                met = qDP.filter(status=SLO_STATUS_CHOICES[0][0]).count()
                metP = met/overall
            else:
                metP = 0 
            name = d.name+" ("+d.level+")"
            try:
                dataFrame[name].append(metP)
            except:
                new = {name:[metP]}
                dataFrame.update(new)
        # for name in dataFrame.keys():
        #     if name is not "Year":
        #         qDP = qYear.filter(report__degreeProgram__name = str(name))
        #         overall = qDP.count()
        #         if overall != 0:
        #             met = qDP.filter(status=SLO_STATUS_CHOICES[0][0]).count()
        #             metP = met/overall
        #         else:
        #             metP = 0
        #         dataFrame[name].append(metP)
        dataFrame['Year'].append(year)
    df = pd.DataFrame(dataFrame)
    yVals = list(dataFrame.keys()).remove('Year')
    lines = df.plot(kind='bar',x='Year',y=yVals)
    lines.set(xlabel="Year", ylabel="Percentage")
    lines.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y))) 
    figure = lines.get_figure()
    return figure
class createGraphAPI(views.APIView):
    """
    JSON API to get url of graph on file server with specified college,
    department, degree program, start and end dates, specific graph choice,
    and maybe SLO to be graphed
    """
    
    def post(self,request,format=None):
        """
        Returns URL to graph on file server upon get request to API

        Args:
            request (HttpRequest): POST request to API
            format (None): format of request (not used here)
        """
        #Start by deleting some old graphs
        graphs = Graph.objects.filter(dateTime__date__lte=datetime.now()-timedelta(minutes=20))
        for g in graphs:
            g.graph.delete(save=False)
            g.delete()
        dec = request.data['decision']
        if dec == '1':
            #specific SLO
            figure = get_specificSLO_graph(request)
        elif dec == '2':
            #Number of SLOs met
            figure = get_numberSLOs_graph(request)
        elif dec == '3':
            #Number of degree programs meeting target
            figure = get_degreeProgramSuccess_graph(request)
        if figure:
            f1 = io.BytesIO()
            figure.savefig(f1, format="png", bbox_inches='tight')
            content_file = files.images.ImageFile(f1)
            graphObj = Graph.objects.create(dateTime=datetime.now())
            graphObj.graph.save("graph-"+str(request.user)+"-"+str(datetime.now())+".png",content_file)
            return Response(graphObj.graph.url)
        else:
            return Response("error",status.HTTP_404_NOT_FOUND)


