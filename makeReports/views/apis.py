from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework import serializers
from makeReports.models import *

class DeptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = ['pk','name']
class DeptByColListAPI(generics.ListAPIView):
    queryset = Department.active_objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (['college'])
    serializer_class = DeptSerializer


