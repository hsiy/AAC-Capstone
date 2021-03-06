# Generated by Django 2.2.5 on 2019-12-14 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makeReports', '0002_auto_20191203_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='numberOfUses',
            field=models.PositiveIntegerField(default=0, verbose_name='number of uses'),
        ),
        migrations.AlterField(
            model_name='gradedrubricitem',
            name='grade',
            field=models.CharField(choices=[('DNM', 'Does Not Meet/Did Not Include'), ('MC', 'Meets with Concerns'), ('ME', 'Meets Established')], max_length=300),
        ),
        migrations.AlterField(
            model_name='slo',
            name='numberOfUses',
            field=models.PositiveIntegerField(default=0, verbose_name='number of uses of this SLO'),
        ),
    ]
