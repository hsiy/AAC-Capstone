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
import io
from datetime import datetime, timedelta

class DeptSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes departments to JSON with the primary key and name
    """
    class Meta:
        """
        Defines the model type and fields for the superclass
        to use to build the serializer.
        """
        model = Department
        fields = ['pk','name']
class ProgSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes degree programs to JSON with the primary key, name, and level
    """
    class Meta:
        """
        Defines the model type and fields for the superclass
        to use to build the serializer
        """
        model = DegreeProgram
        fields = ['pk', 'name', 'level']
class SLOserializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes SLOs to JSON with the primary key and name
    """
    class Meta:
        """
        Defines the model type and fields for the superclass
        to use to build the serializer
        """
        model = SLOInReport
        fields = ['pk', 'goalText']
class SLOParentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes :class:`~makeReports.models.SLO` into just its primary key
    """
    class Meta:
        """
        Defines the model type and fields for the superclass
        to use to build the serializer
        """
        model = SLO
        fields = ['pk']
class SLOSerializerWithParent(serializers.HyperlinkedModelSerializer):
    """
    Serializes SLOs (:class:`~makeReports.models.SLOInReport`) to JSON with the primary key and name and primary key of SLO
    """
    slo = SLOParentSerializer()
    class Meta:
        """
        Defines the model type and fields for the superclass
        to use to build the serializer
        """
        model = SLOInReport
        fields = ['pk', 'goalText','slo']
class AssessmentParentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes parent assessments (:class:`~makeReports.models.Assessment`) into its primary key and title
    """
    class Meta:
        """
        Defines the model type and fields for the superclass
        to use to build the serializer
        """
        model = Assessment
        fields = ['pk','title']
class Assessmentserializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes assessments (:class:`~makeReports.models.AssessmentVersion`) to JSON with the primary key and and title
    """
    assessment =AssessmentParentSerializer()
    class Meta:
        """
        Defines the model type and fields for the superclass
        to use to build the serializer
        """
        model = SLOInReport
        fields = ['pk', 'assessment']
class FileSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializes graphs to JSON with all fields 
    """
    class Meta:
        """
        Defines the model type and fields for the superclass
        to use to build the serializer
        """
        model = Graph
        fields = "__all__"
