# Generated by Django 2.2.5 on 2019-10-13 16:30

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('makeReports', '0038_gradgoal_active'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='gradgoal',
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
