# Generated by Django 4.0.5 on 2022-10-12 17:16

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mySchoolapp', '0038_studentdetails_session_alter_attendance_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherdetails',
            name='session',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mySchoolapp.sessioninfo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subjectfile',
            name='date_uploaded',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 12, 6, 16, 51, 319951)),
        ),
    ]