# Generated by Django 4.0.5 on 2022-10-06 18:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySchoolapp', '0025_rename_assignment_solution_file_assignmentsolution_solution_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentsolution',
            name='number_of_submission',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateTimeField(default=datetime.date(2022, 10, 6)),
        ),
    ]