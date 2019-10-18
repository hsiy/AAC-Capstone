# Generated by Django 2.2.5 on 2019-10-06 23:57

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('makeReports', '0025_auto_20191005_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataadditionalinformation',
            name='supplement',
            field=models.FileField(default=None, storage=gdstorage.storage.GoogleDriveStorage(), upload_to='data/supplements'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='DataAddInfoSupplement',
        ),
    ]