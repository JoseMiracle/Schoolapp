# Generated by Django 4.0.5 on 2022-10-02 23:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySchoolapp', '0020_rename_student_name_assignmentsolution_student_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsolution',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateTimeField(default=datetime.date(2022, 10, 2)),
        ),
    ]
