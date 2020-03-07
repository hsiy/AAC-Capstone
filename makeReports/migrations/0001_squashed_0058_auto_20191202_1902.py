# Generated by Django 2.2.5 on 2019-12-03 21:05

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import gdstorage.storage


class Migration(migrations.Migration):
    
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
            ],
        ),     
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makeReports.College')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DegreeProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('level', models.CharField(choices=[('UG', 'Undergraduate'), ('GR', 'Graduate')], max_length=75)),
                ('cycle', models.IntegerField(blank=True, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makeReports.Department')),
                ('startingYear', models.PositiveIntegerField(blank=True, null=True, verbose_name='starting year of cycle')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rubric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('fullFile', models.FileField(blank=True, default='settings.STATIC_ROOT/norubric.pdf', null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to='rubrics', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('pdf',))], verbose_name='rubric file')),
                ('name', models.CharField(default='Rubric', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='GradGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(choices=[(1, 'Something'), (2, 'Something else')], max_length=300)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SLO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blooms', models.CharField(choices=[('KN', 'Knowledge'), ('CO', 'Comprehension'), ('AP', 'Application'), ('AN', 'Analysis'), ('SN', 'Synthesis'), ('EV', 'Evaluation')], max_length=50, verbose_name="Bloom's taxonomy level")),
                ('gradGoals', models.ManyToManyField(to='makeReports.GradGoal', verbose_name='graduate-level goals')),
                ('numberOfUses', models.PositiveIntegerField(default=1, verbose_name='number of uses of this SLO')),
            ],
        ),
        migrations.CreateModel(
            name='GradedRubric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rubricVersion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makeReports.Rubric', verbose_name='rubric version')),
                ('generalComment', models.CharField(blank=True, max_length=2000, null=True, verbose_name='general comment')),
                ('section1Comment', models.CharField(blank=True, max_length=2000, null=True, verbose_name='section I comment')),
                ('section2Comment', models.CharField(blank=True, max_length=2000, null=True, verbose_name='section II comment')),
                ('section3Comment', models.CharField(blank=True, max_length=2000, null=True, verbose_name='section III comment')),
                ('section4Comment', models.CharField(blank=True, max_length=2000, null=True, verbose_name='section IV comment')),
                ('complete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(blank=True, max_length=100)),
                ('section1Comment', models.CharField(blank=True, max_length=2000, null=True, verbose_name='section I comment')),
                ('section2Comment', models.CharField(blank=True, max_length=2000, null=True, verbose_name='section II comment')),
                ('section3Comment', models.CharField(blank=True, max_length=2000, null=True, verbose_name='section III comment')),
                ('section4Comment', models.CharField(blank=True, max_length=2000, null=True, verbose_name='section IV comment')),
                ('submitted', models.BooleanField()),
                ('degreeProgram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makeReports.DegreeProgram', verbose_name='degree program')),
                ('rubric', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='makeReports.GradedRubric')),
                ('year', models.PositiveIntegerField(default=2019)),
                ('returned', models.BooleanField(default=False)),
                ('date_range_of_reported_data', models.CharField(blank=True, max_length=500, null=True)),
                ('numberOfSLOs', models.PositiveIntegerField(default=0, verbose_name='number of SLOs')),
            ],
        ),
        migrations.CreateModel(
            name='SLOInReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makeReports.Report')),
                ('slo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makeReports.SLO', verbose_name='SLO')),
                ('changedFromPrior', models.BooleanField(verbose_name='changed from prior version')),
                ('date', models.DateField(default=datetime.datetime(2019, 9, 28, 18, 22, 15, 5314))),
                ('goalText', models.CharField(max_length=1000, verbose_name='goal text')),
                ('number', models.PositiveIntegerField(default=1)),
                ('numberOfAssess', models.PositiveIntegerField(default=0, verbose_name='number of assessments')),
            ],
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('domainExamination', models.BooleanField(verbose_name='examination domain')),
                ('domainProduct', models.BooleanField(verbose_name='product domain')),
                ('domainPerformance', models.BooleanField(verbose_name='performance domain')),
                ('directMeasure', models.BooleanField(verbose_name='direct measure')),
                ('numberOfUses', models.PositiveIntegerField(default=1, verbose_name='number of uses')),
            ],
        ),
        
        migrations.CreateModel(
            name='DataAdditionalInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, default='', max_length=3000)),
                ('report', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='makeReports.Report')),
                ('supplement', models.FileField(storage=gdstorage.storage.GoogleDriveStorage(), upload_to='data/supplements', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('pdf',))])),
            ],
        ),


        migrations.CreateModel(
            name='SLOStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Met', 'Met'), ('Partially Met', 'Partially Met'), ('Not Met', 'Not Met'), ('Unknown', 'Unknown')], max_length=50)),
                ('sloIR', models.OneToOneField(default=4, on_delete=django.db.models.deletion.CASCADE, to='makeReports.SLOInReport')),
                ('override', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ResultCommunicate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=3000)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makeReports.Report')),
            ],
        ),
        migrations.CreateModel(
            name='DecisionsActions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, default='', max_length=3000)),
                ('sloIR', models.OneToOneField(default=3, on_delete=django.db.models.deletion.CASCADE, to='makeReports.SLOInReport')),
            ],
        ),
        migrations.CreateModel(
            name='SLOsToStakeholder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=2000)),
                ('report', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='makeReports.Report')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aac', models.BooleanField(null=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='makeReports.Department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RubricItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('section', models.PositiveIntegerField(choices=[(1, 'I. Student Learning Outcomes'), (2, 'II. Assessment Methods'), (3, 'III. Data Collection and Analysis'), (4, 'IV. Decisions and Actions')])),
                ('rubricVersion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makeReports.Rubric', verbose_name='rubric version')),
                ('order', models.PositiveIntegerField(blank=True, null=True)),
                ('DMEtext', models.CharField(blank=True, default='', max_length=1000, verbose_name='did not meet expectations text')),
                ('EEtext', models.CharField(blank=True, default='', max_length=1000, verbose_name='exceeded expecations text')),
                ('MEtext', models.CharField(blank=True, default='', max_length=1000, verbose_name='met expectations text')),
                ('abbreviation', models.CharField(blank=True, default='', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='GradedRubricItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(choices=[('DNM', 'Does Not Meet/Did Not Include'), ('MC', 'Meets with Concerns'), ('ME', 'Meets')], max_length=300)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makeReports.RubricItem')),
                ('rubric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makeReports.GradedRubric')),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentSupplement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplement', models.FileField(storage=gdstorage.storage.GoogleDriveStorage(), upload_to='asssements/supplements', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('pdf',))])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2019, 10, 3, 14, 23, 13, 368164))),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.CharField(max_length=1000)),
                ('finalTerm', models.BooleanField(verbose_name='final term')),
                ('where', models.CharField(max_length=500, verbose_name='location of assessment')),
                ('allStudents', models.BooleanField(verbose_name='all students assessed')),
                ('sampleDescription', models.CharField(blank=True, max_length=500, null=True, verbose_name='description of sample')),
                ('frequency', models.CharField(max_length=100)),
                ('threshold', models.CharField(max_length=500)),
                ('target', models.PositiveIntegerField()),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makeReports.Assessment')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makeReports.Report')),
                ('changedFromPrior', models.BooleanField(verbose_name='changed from prior version')),
                ('slo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makeReports.SLOInReport', verbose_name='SLO in report')),
                ('supplements', models.ManyToManyField(to='makeReports.AssessmentSupplement')),
                ('number', models.PositiveIntegerField(default=0)),
                ('frequencyChoice', models.CharField(choices=[('O', 'Other'), ('S', 'Once/semester'), ('Y', 'Once/year')], default='O', max_length=100, verbose_name='frequency choice')),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numberStudents', models.PositiveIntegerField(verbose_name='number of students')),
                ('overallProficient', models.PositiveIntegerField(blank=True, verbose_name='overall percentage proficient')),
                ('assessmentVersion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makeReports.AssessmentVersion', verbose_name='assessment version')),
                ('dataRange', models.CharField(max_length=500, verbose_name='data range')),
            ],
        ),
        migrations.CreateModel(
            name='ReportSupplement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplement', models.FileField(storage=gdstorage.storage.GoogleDriveStorage(), upload_to='data/supplements', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('pdf',))])),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makeReports.Report')),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=2000)),
                ('expiration', models.DateField()),
                ('creation', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelManagers(
            name='gradgoal',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='gradgoal',
            name='text',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='gradgoal',
            name='text',
            field=models.CharField(max_length=600),
        ),
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField()),
                ('graph', models.FileField(storage=gdstorage.storage.GoogleDriveStorage(), upload_to='data/graphs')),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentAggregate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aggregate_proficiency', models.PositiveIntegerField(verbose_name='aggregate proficiency percentage')),
                ('met', models.BooleanField(verbose_name='target met')),
                ('assessmentVersion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='makeReports.AssessmentVersion', verbose_name='assessment version')),
                ('override', models.BooleanField(default=False)),
            ],
        ),
    ]
