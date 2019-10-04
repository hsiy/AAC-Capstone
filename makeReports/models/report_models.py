from django.db import models
from makeReports.choices import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from gdstorage.storage import GoogleDriveStorage
from datetime import datetime
import os
gd_storage = GoogleDriveStorage()
class NonArchivedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)
class Report(models.Model):
    year = models.PositiveIntegerField()
    author = models.CharField(max_length=100, blank=True)
    degreeProgram = models.ForeignKey('DegreeProgram', on_delete=models.CASCADE)
    date_range_of_reported_data = models.CharField(max_length=500,blank=True, null=True)
    rubric = models.OneToOneField('GradedRubric', on_delete=models.SET_NULL, null=True)
    section1Comment = models.CharField(max_length=2000, blank=True, null=True)
    section2Comment = models.CharField(max_length=2000, blank=True, null=True)
    section3Comment = models.CharField(max_length=2000, blank=True, null=True)
    section4Comment = models.CharField(max_length=2000, blank=True, null=True)
    submitted = models.BooleanField()
    returned = models.BooleanField(default=False)
class College(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = NonArchivedManager()
    def __str__(self):
        return self.name
class Department(models.Model):
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = NonArchivedManager()    
    def __str__(self):
        return self.name
class DegreeProgram(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=75, choices= LEVELS)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    cycle = models.IntegerField(blank=True, null=True)
    startingYear = models.PositiveIntegerField(blank=True, null=True)
    #not all degree programs are on a clear cycle
    active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = NonArchivedManager()
    def __str__(self):
        return self.name
class SLO(models.Model):
    blooms = models.CharField(choices=BLOOMS_CHOICES,max_length=50)
    gradGoals = models.ManyToManyField('GradGoal')
class SLOInReport(models.Model):
    date = models.DateField()
    goalText = models.CharField(max_length=600)
    slo = models.ForeignKey(SLO, on_delete=models.CASCADE)    
    firstInstance = models.BooleanField()
    changedFromPrior = models.BooleanField()
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    def __str__(self):
        return self.goalText
class GradGoal(models.Model):
    text = models.CharField(max_length=300, choices=GRAD_GOAL_CHOICES)
    def __str__(self):
        return self.text
class SLOsToStakeholder(models.Model):
    text = models.CharField(max_length=2000)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.text
class Assessment(models.Model):
    title = models.CharField(max_length=300)
    domainExamination = models.BooleanField()
    domainProduct = models.BooleanField()
    domainPerformance = models.BooleanField()
    directMeasure = models.BooleanField()
    #false = indirect measure
    def __str__(self):
        return self.title
class AssessmentVersion(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    slo = models.ForeignKey(SLOInReport, on_delete=models.CASCADE)
    firstInstance = models.BooleanField()
    changedFromPrior = models.BooleanField()
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=1000)
    finalTerm = models.BooleanField()
    #false = final year
    where = models.CharField(max_length=200)
    allStudents = models.BooleanField()
    #false = sample of students
    sampleDescription = models.CharField(max_length=200)
    frequency = models.CharField(max_length=100)
    #the below are percentage points
    threshold = models.PositiveIntegerField()
    target = models.PositiveIntegerField()
    def __str__(self):
        return self.text
class AssessmentSupplement(models.Model):
    assessmentVersion = models.ForeignKey(AssessmentVersion,on_delete=models.CASCADE)
    supplement = models.FileField(upload_to='asssements/supplements', storage=gd_storage)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return os.path.basename(supplement.name)
class Subassessment(models.Model):
    assessmentVersion = models.ForeignKey(AssessmentVersion, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
class AssessmentData(models.Model):
    assessmentVersion = models.ForeignKey(AssessmentVersion,on_delete=models.CASCADE)
    dataBegin = models.DateField()
    dataEnd = models.DateField()
    numberStudents = models.PositiveIntegerField()
    overallProficient = models.PositiveIntegerField(blank=True)
class SubassessmentData(models.Model):
    subassessment = models.ForeignKey(Subassessment,on_delete=models.CASCADE)
    proficient = models.PositiveIntegerField()
class DataAdditionalInformation(models.Model):
    comment = models.CharField(max_length=3000, blank=True)
class DataAddInfoSupplement(models.Model):
    supplement = models.FileField(upload_to='data/supplements', storage=gd_storage)
    addInfo = models.ForeignKey(DataAdditionalInformation, on_delete=models.CASCADE)
class SLOStatus(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    SLO = models.ForeignKey(SLO, on_delete=models.CASCADE)
class ResultCommunicate(models.Model):
    text = models.CharField(max_length=3000)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
class DecisionsActions(models.Model):
    SLO = models.ForeignKey(SLO, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    decisionProcess = models.CharField(max_length=3000)
    decisionMakers = models.CharField(max_length=3000)
    decisionTimeline = models.CharField(max_length=3000)
    dataUsed = models.CharField(max_length=3000)
    actionTimeline = models.CharField(max_length=3000)
class Rubric(models.Model):
    date = models.DateField()
    fullFile = models.FileField(upload_to='rubrics', storage=gd_storage)
    name = models.CharField(max_length = 150, default="Rubric")
    def __str__(self):
        return self.name
class GradedRubric(models.Model):
    rubricVersion = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    section1Comment = models.CharField(max_length=2000,blank=True,null=True)
    section2Comment = models.CharField(max_length=2000,blank=True,null=True)
    section3Comment = models.CharField(max_length=2000,blank=True,null=True)
    section4Comment = models.CharField(max_length=2000,blank=True,null=True)
    generalComment = models.CharField(max_length=2000,blank=True,null=True)
    complete = models.BooleanField(default=False)
class RubricItem(models.Model):
    text = models.CharField(max_length=1000)
    section = models.PositiveIntegerField(choices=SECTIONS)
    rubricVersion = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(null=True, blank=True)
    DMEtext = models.CharField(max_length=1000, default="", blank=True)
    MEtext = models.CharField(max_length=1000, default="", blank=True)
    EEtext = models.CharField(max_length=1000, default="", blank=True)
class GradedRubricItem(models.Model):
    rubric = models.ForeignKey('GradedRubric', on_delete=models.CASCADE)
    item = models.ForeignKey(RubricItem, on_delete=models.PROTECT)
    grade = models.CharField(max_length=300, choices=RUBRIC_GRADES_CHOICES)
class ReportSupplement(models.Model):
    supplement = models.FileField(upload_to='data/supplements', storage=gd_storage)
    report = models.ForeignKey('Report', on_delete=models.CASCADE)
    def __str__(self):
        return os.path.basename(supplement.name)
#to be added: classes for messaging system
class Profile(models.Model):
    #first name, last name and email are included in the built-in User class. Access them through the user field
    aac = models.BooleanField(null=True)
    #False = faculty member/dept account
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
@receiver(post_save,sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    #this updates profile when user is updated
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()