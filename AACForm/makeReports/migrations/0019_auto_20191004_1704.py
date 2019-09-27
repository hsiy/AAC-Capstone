# Generated by Django 2.2.5 on 2019-10-04 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('makeReports', '0018_auto_20191004_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataadditionalinformation',
            name='report',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='makeReports.Report'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rubric',
            name='name',
            field=models.CharField(default='Rubric 2019-10-04 17:03:59.216541', max_length=150),
        ),
    ]