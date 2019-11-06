"""
Includes all models used in application, which act both as Python objects and abstractions for database items
"""
from django.db import models
from makeReports.choices import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from gdstorage.storage import GoogleDriveStorage
from django.core.validators import FileExtensionValidator
from django.utils.safestring import mark_safe
import os

gd_storage = GoogleDriveStorage()
class NonArchivedManager(models.Manager):
    """
    Includes only active objects
    """
    def get_queryset(self):
        """
        Retrieves only active objects within type

        Returns:
            QuerySet : active objects only
        """
        return super().get_queryset().filter(active=True)
class Report(models.Model):
    """
    Report model which collects attributes specific to a report and completion status
    """
    year = models.PositiveIntegerField()
    author = models.CharField(max_length=100, blank=True)
    degreeProgram = models.ForeignKey('DegreeProgram', on_delete=models.CASCADE, verbose_name="degree program")
    date_range_of_reported_data = models.CharField(max_length=500,blank=True, null=True)
    rubric = models.OneToOneField('GradedRubric', on_delete=models.SET_NULL, null=True)
    section1Comment = models.CharField(max_length=2000, blank=True, null=True, verbose_name="section I comment")
    section2Comment = models.CharField(max_length=2000, blank=True, null=True, verbose_name="section II comment")
    section3Comment = models.CharField(max_length=2000, blank=True, null=True, verbose_name="section III comment")
    section4Comment = models.CharField(max_length=2000, blank=True, null=True, verbose_name="section IV comment")
    submitted = models.BooleanField()
    returned = models.BooleanField(default=False)
    numberOfSLOs = models.PositiveIntegerField(default=0, verbose_name="number of SLOs")
class College(models.Model):
    """
    College model for colleges within the university
    """
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = NonArchivedManager()
    def __str__(self):
        return self.name
class Department(models.Model):
    """
    Department model for departments within colleges 
    """
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = NonArchivedManager()    
    def __str__(self):
        return self.name
class DegreeProgram(models.Model):
    """
    Degree program model for degree programs within departments
    """
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=75, choices= LEVELS)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    cycle = models.IntegerField(blank=True, null=True)
    startingYear = models.PositiveIntegerField(blank=True, null=True, verbose_name="starting year of cycle")
    #not all degree programs are on a clear cycle
    active = models.BooleanField(default=True)
    objects = models.Manager()
    active_objects = NonArchivedManager()
    def __str__(self):
        return self.name
class SLO(models.Model):
    """
    Model collects SLO in reports which are ostensibly  the same except minor changes, 
    includes only the attributes which should never change and counts how often it is used
    """
    blooms = models.CharField(choices=BLOOMS_CHOICES,max_length=50, verbose_name="Bloom's taxonomy level")
    gradGoals = models.ManyToManyField('GradGoal', verbose_name="graduate-level goals")
    numberOfUses = models.PositiveIntegerField(default=1, verbose_name="number of uses of this SLO")
class SLOInReport(models.Model):
    """
    A specific version of an SLO which occurs within a report
    """
    date = models.DateField()
    goalText = models.CharField(max_length=1000, verbose_name="goal text")
    slo = models.ForeignKey(SLO, on_delete=models.CASCADE, verbose_name="SLO")    
    changedFromPrior = models.BooleanField(verbose_name="changed from prior version")
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=1)
    numberOfAssess = models.PositiveIntegerField(default=0, verbose_name="number of assessments")
    def __str__(self):
        return self.goalText
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
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return mark_safe(self.text)
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
    numberOfUses = models.PositiveIntegerField(default=1, verbose_name="number of uses")
    #false = indirect measure
    def __str__(self):
        return self.title
class AssessmentVersion(models.Model):
    """
    Specific versions of Assessments that occur within a report
    """
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    slo = models.ForeignKey(SLOInReport, on_delete=models.CASCADE, verbose_name="SLO in report")
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
class Subassessment(models.Model):
    """
    Subassessment for data collection
    """
    assessmentVersion = models.ForeignKey(AssessmentVersion, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    proficient = models.PositiveIntegerField()
class AssessmentData(models.Model):
    """
    Assessment data point for a particular assessment in a report
    """
    assessmentVersion = models.ForeignKey(AssessmentVersion,on_delete=models.CASCADE, verbose_name="assessment version")
    dataRange = models.CharField(max_length=500, verbose_name="data range")
    numberStudents = models.PositiveIntegerField(verbose_name="number of students")
    overallProficient = models.PositiveIntegerField(blank=True, verbose_name="overall percentage proficient")
class AssessmentAggregate(models.Model):
    """
    Aggregates the various assessments on different ranges for an aggregate success rate
    """ 
    assessmentVersion = models.ForeignKey(AssessmentVersion, on_delete=models.CASCADE, verbose_name="assessment version")
    aggregate_proficiency = models.PositiveIntegerField(verbose_name="aggregate proficiency percentage")
    met = models.BooleanField(verbose_name="target met")
    def __str__(self):
        return str(self.aggregate_proficiency)
class DataAdditionalInformation(models.Model):
    """
    Model to hold additional information about the data, possibly with a PDF supplement
    """
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
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
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=SLO_STATUS_CHOICES)
    SLO = models.ForeignKey(SLO, on_delete=models.CASCADE)
class ResultCommunicate(models.Model):
    """
    Model holds the text for communicating results
    """
    text = models.CharField(max_length=3000)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
class DecisionsActions(models.Model):
    """
    Model of decisions/actions for a report
    """
    SLO = models.ForeignKey(SLO, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    text = models.CharField(max_length=3000, blank=True, default="")
    decisionProcess = models.CharField(max_length=3000, blank=True, default="")
    decisionMakers = models.CharField(max_length=3000, blank=True, default="")
    decisionTimeline = models.CharField(max_length=3000, blank=True, default="")
    dataUsed = models.CharField(max_length=3000, blank=True, default="")
    actionTimeline = models.CharField(max_length=3000, blank=True, default="")
class Rubric(models.Model):
    """
    Model of rubric to collect rubric items and hold a file
    """
    date = models.DateField()
    fullFile = models.FileField(
        default='settings.STATIC_ROOT/norubric.pdf',
        verbose_name="rubric file",
        upload_to='rubrics', 
        storage=gd_storage, 
        null=True,
        blank=True, 
        validators=[FileExtensionValidator(allowed_extensions=('pdf',))])
    name = models.CharField(max_length = 150, default="Rubric")
    def __str__(self):
        return self.name
class GradedRubric(models.Model):
    """
    Model to collect graded rubric items and comments on a report
    """
    rubricVersion = models.ForeignKey(Rubric, on_delete=models.CASCADE, verbose_name="rubric version")
    section1Comment = models.CharField(max_length=2000,blank=True,null=True, verbose_name="section I comment")
    section2Comment = models.CharField(max_length=2000,blank=True,null=True, verbose_name="section II comment")
    section3Comment = models.CharField(max_length=2000,blank=True,null=True, verbose_name="section III comment")
    section4Comment = models.CharField(max_length=2000,blank=True,null=True, verbose_name="section IV comment")
    generalComment = models.CharField(max_length=2000,blank=True,null=True, verbose_name="general comment")
    complete = models.BooleanField(default=False)
    def __str__(self):
        return self.rubricVersion.name
class RubricItem(models.Model):
    """
    Model of individual items within a rubric
    """
    text = models.CharField(max_length=1000)
    section = models.PositiveIntegerField(choices=SECTIONS)
    rubricVersion = models.ForeignKey(Rubric, on_delete=models.CASCADE, verbose_name="rubric version")
    order = models.PositiveIntegerField(null=True, blank=True)
    abbreviation = models.CharField(max_length=20, default="", blank=True)
    DMEtext = models.CharField(max_length=1000, default="", blank=True, verbose_name="did not meet expectations text")
    MEtext = models.CharField(max_length=1000, default="", blank=True, verbose_name="met expectations text")
    EEtext = models.CharField(max_length=1000, default="", blank=True, verbose_name="exceeded expecations text")
    def __str__(self):
        return mark_safe(self.text)
class GradedRubricItem(models.Model):
    """
    Model individual items within a graded rubric
    """
    rubric = models.ForeignKey('GradedRubric', on_delete=models.CASCADE)
    item = models.ForeignKey(RubricItem, on_delete=models.CASCADE)
    grade = models.CharField(max_length=300, choices=RUBRIC_GRADES_CHOICES)
class ReportSupplement(models.Model):
    """
    Model to hold supplements to the report as a whole
    """
    supplement = models.FileField(
        upload_to='data/supplements', 
        storage=gd_storage,
        validators=[FileExtensionValidator(allowed_extensions=('pdf',))])
    report = models.ForeignKey('Report', on_delete=models.CASCADE)
    def __str__(self):
        return os.path.basename(self.supplement.name)
class Announcement(models.Model):
    """
    Model to hold annnoucements the AAC make
    """
    text = models.CharField(max_length=2000,blank=True)
    expiration = models.DateField()
    creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return mark_safe(self.text)
class Profile(models.Model):
    """
    Model to hold extra information in addition to Django's User class, including whether they are 
    AAC members and the department
    """
    #first name, last name and email are included in the built-in User class. Access them through the user field
    aac = models.BooleanField(null=True)
    #False = faculty member/dept account
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
@receiver(post_save,sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    Updates the custom profile when users are created
    
    Args:
        sender (User): model sending hook
        instance (User): user updated
        created (Boolean): whether model was newly created
    """
    #this updates profile when user is updated
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()