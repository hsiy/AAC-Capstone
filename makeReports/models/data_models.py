"""
This file contains models most directly related to data from assessments
"""
from django.db import models
from makeReports.choices import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from gdstorage.storage import GoogleDriveStorage
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe
import os
from .basic_models import gd_storage

class AssessmentData(models.Model):
    """
    Assessment data point for a particular assessment in a report
    """
    assessmentVersion = models.ForeignKey('AssessmentVersion',on_delete=models.CASCADE, verbose_name="assessment version")
    dataRange = models.CharField(max_length=500, verbose_name="data range")
    numberStudents = models.PositiveIntegerField(verbose_name="number of students")
    overallProficient = models.PositiveIntegerField(blank=True, verbose_name="overall percentage proficient")

@receiver(post_save,sender=AssessmentData)
def post_save_agg_by_data(sender, instance, **kwargs):
    """
    Updates aggregates when data is created or modified post-save
    
    Args:
        sender (AssessmentData): model sending hook
        instance (AssessmentData): data updated
    """
    update_agg_by_data(sender,instance, 0)
@receiver(pre_delete,sender=AssessmentData)
def pre_delete_agg_by_data(sender,instance,**kwargs):
    """
    Updates aggregates when data is deleted
    
    Args:
        sender (AssessmentData): model sending hook
        instance (AssessmentData): data updated
    """
    update_agg_by_data(sender,instance, 1)
def update_agg_by_data(sender, instance, sigType):
    """
    Updates the assessment aggregate when data is modified or created and it has not been previously overridden
    
    Args:
        sender (AssessmentData): model sending hook
        instance (AssessmentData): data updated
        sigType (int): signal type - 0 if save, 1 if delete
    """
    try:
        agg = AssessmentAggregate.objects.get(assessmentVersion=instance.assessmentVersion)
        if not agg.override:
            agg.aggregate_proficiency = calcWeightedAgg(instance.assessmentVersion, sigType, instance.pk)
            agg.met = (agg.aggregate_proficiency >= instance.assessmentVersion.target)
            agg.save()
    except:
        aProf = calcWeightedAgg(instance.assessmentVersion, sigType, instance.pk)
        met = (aProf >= instance.assessmentVersion.target)
        AssessmentAggregate.objects.create(
            assessmentVersion=instance.assessmentVersion,
            aggregate_proficiency=aProf, 
            met = met)
def calcWeightedAgg(assessment, sigType, pk):
    """
    Calculates the weighted aggregate value based upon assessment data for 
    the given :class:`~makeReports.models.AssessmentVersion`

    Args:
        assessment (~makeReports.models.AssessmentVersion) : the assessment to calculate the aggregate for
        sigType (int): signal type - 0 is post-save, 1 is pre-delete
        pk (int): primary key of instance that changed (only needed if pre-delete)

    Returns:
        int : the weighted aggregate
    """
    data = AssessmentData.objects.filter(assessmentVersion=assessment)
    if sigType == 1:
        data = data.exclude(pk=pk)
    totalStudents = 0
    totalProf = 0
    for dat in data:
        totalStudents += dat.numberStudents
        totalProf += dat.numberStudents*dat.overallProficient
    if totalStudents==0:
        return 0
    return round(totalProf/totalStudents)
class AssessmentAggregate(models.Model):
    """
    Aggregates the various assessments on different ranges for an aggregate success rate
    """ 
    assessmentVersion = models.OneToOneField('AssessmentVersion', on_delete=models.CASCADE, verbose_name="assessment version")
    aggregate_proficiency = models.PositiveIntegerField(verbose_name="aggregate proficiency percentage")
    met = models.BooleanField(verbose_name="target met")
    override = models.BooleanField(default=False)
    def __str__(self):
        return str(self.aggregate_proficiency)
@receiver(post_save,sender=AssessmentAggregate)
def post_save_status_by_agg(sender,instance,**kwargs):
    """
    Updates status based upon aggregates after model is saved

    Args:
        sender (AssessmentAggregate): model sending hook
        instance (AssessmentAggregate): data updated
    """
    update_status_by_agg(sender,instance, 0)
@receiver(pre_delete,sender=AssessmentAggregate)
def pre_delete_status_by_agg(sender,instance,**kwargs):
    """
    Updates status based upon aggregates after model is saved

    Args:
        sender (AssessmentAggregate): model sending hook
        instance (AssessmentAggregate): data updated
    """
    update_status_by_agg(sender,instance,1)

def update_status_by_agg(sender, instance, sigType):
    """
    Updates the SLO status based upon aggregate when aggregates are created or modified
    
    Args:
        sender (AssessmentAggregate): model sending hook
        instance (AssessmentAggregate): data updated
        sigType (int): singal type - 0 is post-save, 1 if pre-delete
    """
    sloIR = instance.assessmentVersion.slo
    try:
        sS = SLOStatus.objects.get(sloIR=sloIR)
        override = sS.override
    except:
        sS = None
        override = False
    if not override:
        aggs = AssessmentAggregate.objects.filter(assessmentVersion__slo=sloIR)
        if sigType==1:
            aggs = aggs.exclude(pk=instance.pk)
        met = True
        partiallyMet = False
        for a in aggs:
            if a.met is False:
                met = False
            if a.met is True:
                partiallyMet=True
            if not met and partiallyMet:
                break
        if sS:
            if met:
                sS.status = SLO_STATUS_CHOICES[0][0]
            elif partiallyMet:
                sS.status = SLO_STATUS_CHOICES[1][0]
            else:
                sS.status = SLO_STATUS_CHOICES[2][0]
            sS.save()
        else:
            if met:
                SLOStatus.objects.create(status=SLO_STATUS_CHOICES[0][0],sloIR=sloIR)
            elif partiallyMet:
                SLOStatus.objects.create(status=SLO_STATUS_CHOICES[1][0],sloIR=sloIR)
            else:
                SLOStatus.objects.create(status=SLO_STATUS_CHOICES[2][0],sloIR=sloIR)
class DataAdditionalInformation(models.Model):
    """
    Model to hold additional information about the data, possibly with a PDF supplement
    """
    report = models.ForeignKey('Report', on_delete=models.CASCADE)
    comment = models.CharField(max_length=3000, blank=True, default="")
    supplement = models.FileField(
        upload_to='data/supplements', 
        storage=gd_storage, 
        validators=[FileExtensionValidator(allowed_extensions=('pdf',))])
    def __str__(self):
        return os.path.basename(self.supplement.name)
class SLOStatus(models.Model):
    """
    Status of whether the target was met for an SLO
    """
    status = models.CharField(max_length=50, choices=SLO_STATUS_CHOICES)
    sloIR = models.OneToOneField('SLOInReport',on_delete=models.CASCADE)
    override = models.BooleanField(default=False)
class ResultCommunicate(models.Model):
    """
    Model holds the text for communicating results
    """
    text = models.CharField(max_length=3000)
    report = models.ForeignKey('Report', on_delete=models.CASCADE)
class Graph(models.Model):
    dateTime = models.DateTimeField()
    graph = models.FileField(
        upload_to='data/graphs', 
        storage=gd_storage,
    )