from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework import serializers
from makeReports.models import *


class DeptSerializer(serializers.HyperlinkedModelSerializer):
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
    queryset = Department.active_objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (['college'])
    serializer_class = DeptSerializer
class ProgByDeptListAPI(generics.ListAPIView):
    queryset = DegreeProgram.active_objects.all()
    filter_backends = (filters.DjangoFilterBackend)
    filterset_fields = (['department'])
    serializer_class = ProgSerializer
class CollsAvailListAPI(generics.ListAPIView):
    queryset = College.active_objects.all()
    serializer_class = CollSerializer
class SloByDeptListAPI(generics.ListAPIView):
    queryset = SLOInReport.active_objects.all()
    filter_backends = (filters.DjangoFilterBackend)
    filterset_fields = (['report.degreeProgram'])
    serializer_class = SLOserializer

