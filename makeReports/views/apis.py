from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework import serializers
from makeReports.models import *
"""
This file contains the JSON APIs used
"""
class DeptSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes departments to JSON with the primary key and name
    """
    class Meta:
        model = Department
        fields = ['pk','name']
class ProgSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DegreeProgram
        fields = ['pk', 'name', 'level']
class SLOserializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SLOInReport
        fields = ['pk', 'name']
class DeptByColListAPI(generics.ListAPIView):
    """
    JSON API to gets active departments within specified college
    """
    queryset = Department.active_objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (['college'])
    serializer_class = DeptSerializer
class ProgByDeptListAPI(generics.ListAPIView):
    queryset = DegreeProgram.active_objects.all()
    filter_backends = (filters.DjangoFilterBackend)
    filterset_fields = (['department'])
    serializer_class = ProgSerializer
class SloByDPListAPI(generics.ListAPIView):
    queryset = SLOInReport.objects.all()
    filter_backends = (filters.DjangoFilterBackend)
    filterset_fields = (['report.degreeProgram'])
    serializer_class = SLOserializer

