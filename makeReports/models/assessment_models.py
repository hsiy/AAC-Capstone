"""
This file contains models most directly related to assessments of SLOs, excluding data collection
"""
from django.db import models
from makeReports.choices import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from gdstorage.storage import GoogleDriveStorage
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe
import os
from .basic_models import gd_storage, NonArchivedManager
from .data_models import AssessmentAggregate

class Assessment(models.Model):
    """
    Assessment model collects assessments that are ostensibly the same except for minor changes,
    and includes fields which should never change
    """
    title = models.CharField(max_length=300)
    domainExamination = models.BooleanField(verbose_name="examination domain")
    domainProduct = models.BooleanField(verbose_name="product domain")
    domainPerformance = models.BooleanField(verbose_name="performance domain")
    directMeasure = models.BooleanField(verbose_name="direct measure")
    numberOfUses = models.PositiveIntegerField(default=0, verbose_name="number of uses")
    #false = indirect measure
    def __str__(self):
        return self.title
class AssessmentVersion(models.Model):
    """
    Specific versions of Assessments that occur within a report
    """
    report = models.ForeignKey('Report', on_delete=models.CASCADE)
    slo = models.ForeignKey('SLOInReport', on_delete=models.CASCADE, verbose_name="SLO in report")
    number = models.PositiveIntegerField(default=0)
    changedFromPrior = models.BooleanField(verbose_name="changed from prior version")
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=1000)
    finalTerm = models.BooleanField(verbose_name="final term")
    #false = final year
    where = models.CharField(max_length=500, verbose_name="location of assessment")
    allStudents = models.BooleanField(verbose_name="all students assessed")
    #false = sample of students
    sampleDescription = models.CharField(max_length=500,blank=True,null=True, verbose_name="description of sample")
    frequencyChoice = models.CharField(max_length=100,choices=FREQUENCY_CHOICES,default="O", verbose_name="frequency choice")
    frequency = models.CharField(max_length=100)
    #the below are percentage points
    threshold = models.CharField(max_length=500)
    target = models.PositiveIntegerField()
    supplements = models.ManyToManyField('AssessmentSupplement')
    def __str__(self):
        return self.assessment.title
def post_create_update_assessment_uses(instance):
    """
    After an assessment version is created, increment the number of uses of Assessment by 1

    Args:
        instance (AssessmentVersion): assessment updated
    """
    instance.assessment.numberOfUses += 1
    instance.slo.numberOfAssess += 1
    instance.assessment.save()
    instance.slo.save()


def post_save_update_agg_by_assessment(instance):
    """
    Updates aggregate (AssessmentAggregate) when AssessmentVersion is changed, in case the target value changed
    
    Args:
        instance (AssessmentVersion): assessment updated
    """
    try:
        aa = instance.assessmentaggregate
        if aa and not aa.override:
            met = (aa.aggregate_proficiency >= instance.target)
            if not (met == aa.met):
                aa.met = met
                aa.save()
    except:
        pass

@receiver(post_save,sender=AssessmentVersion)
def post_save_receiver_assessment(sender,instance,created,**kwargs):
    """
    Post save receiver that triggers aggregates and numbers to be updated
    
    Args:
        sender (type): model type sending hook
        instance (AssessmentVersion): assessment updated
        created (bool): whether model was newly created
    """
    post_save_update_agg_by_assessment(instance)
    if created:
        post_create_update_assessment_uses(instance)
    

@receiver(post_delete,sender=AssessmentVersion)
def post_delete_assessment_update_numbering(sender, instance, **kwargs):
    """
    Updates the numbering of assessments in the same report

    Args:
        sender (type): model type sending hook
        instance (AssessmentVersion): assessment deleted
    """
    assessment = instance.assessment
    slo = instance.slo
    oldNum = instance.number
    if assessment.numberOfUses <= 1:
        assessment.delete()
        assessment.save()
    else:
        assessment.numberOfUses -= 1
        assessment.save()
    assess = AssessmentVersion.objects.filter(report=instance.report,slo=slo)
    for a in assess:
        if a.number > oldNum:
            a.number -= 1
            a.save()
    slo.numberOfAssess -= 1
    slo.save()
class AssessmentSupplement(models.Model):
    """
    Supplemental PDF files to assessments
    """
    supplement = models.FileField(
        upload_to='asssements/supplements', 
        storage=gd_storage, 
        validators=[FileExtensionValidator(allowed_extensions=('pdf',))])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return os.path.basename(self.supplement.name)
