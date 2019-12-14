"""
This file contains models most directly related to Student Learning Outcomes
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

class SLO(models.Model):
    """
    Model collects SLO in reports which are ostensibly  the same except minor changes, 
    includes only the attributes which should never change and counts how often it is used
    """
    blooms = models.CharField(choices=BLOOMS_CHOICES,max_length=50, verbose_name="Bloom's taxonomy level")
    gradGoals = models.ManyToManyField('GradGoal', verbose_name="graduate-level goals")
    numberOfUses = models.PositiveIntegerField(default=0, verbose_name="number of uses of this SLO")
class SLOInReport(models.Model):
    """
    A specific version of an SLO which occurs within a report
    """
    date = models.DateField()
    goalText = models.CharField(max_length=1000, verbose_name="goal text")
    slo = models.ForeignKey(SLO, on_delete=models.CASCADE, verbose_name="SLO")    
    changedFromPrior = models.BooleanField(verbose_name="changed from prior version")
    report = models.ForeignKey('Report', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=1)
    numberOfAssess = models.PositiveIntegerField(default=0, verbose_name="number of assessments")
    def __str__(self):
        return self.goalText
@receiver(post_save,sender=SLOInReport)
def post_save_slo_update_numbering(sender,instance,created,**kwargs):
    """
    Post save receiver that triggers numbers to be updated

    Args:
        sender (type): model type sending hook
        instance (SLOInReport): SLO updated
        created (bool): whether model was newly created
    """
    if created:
        instance.report.numberOfSLOs +=1
        instance.report.save()
        instance.slo.numberOfUses += 1
        instance.slo.save()

@receiver(post_delete,sender=SLOInReport)
def post_delete_slo_update_numbering(sender,instance,**kwargs):
    """
    Updates the numbering of SLOs in the same report

    Args:
        sender (type): model type sending hook
        instance (SLOInReport): SLO deleted
    """
    oldNum = instance.number
    num = instance.report.numberOfSLOs
    if instance.slo.numberOfUses <= 1:
        instance.slo.delete()
    else:
        instance.slo.numberOfUses -= 1
        instance.slo.save()
    slos = SLOInReport.objects.filter(report=instance.report).order_by("number")
    for slo in slos:
        if slo.number > oldNum:
            slo.number -= 1
            slo.save()
    instance.report.numberOfSLOs -= 1
    instance.report.save()

class GradGoal(models.Model):
    """
    A graduate goal graduate level programs may obtain
    """
    text = models.CharField(max_length=600)
    active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = NonArchivedManager()
    def __str__(self):
        return mark_safe(self.text)
class SLOsToStakeholder(models.Model):
    """
    Text describing how SLOs are communicated to stakeholders
    """
    text = models.CharField(max_length=2000)
    report = models.ForeignKey('Report', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return mark_safe(self.text)