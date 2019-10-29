from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from makeReports.models import *
from makeReports.views.helperFunctions import text_processing
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class DeptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = ['pk','name']
class DeptByColListAPI(generics.ListAPIView):
    queryset = Department.active_objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (['college'])
    serializer_class = DeptSerializer


class SLOSuggestionsAPI(APIView):
    renderer_classes = [JSONRenderer]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        slo_text = request.data['slo_text']
        response = text_processing.create_suggestions_dict(slo_text)
        return(Response(response))