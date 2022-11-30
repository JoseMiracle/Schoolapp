# Generated by Django 4.0.5 on 2022-10-02 02:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mySchoolapp', '0018_rename_title_subjectfile_file_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateTimeField(default=datetime.date(2022, 10, 1)),
        ),
        migrations.CreateModel(
            name='AssignmentSolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=100)),
                ('assignment_solution_file', models.FileField(upload_to='')),
                ('subject_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mySchoolapp.subjectfile')),
            ],
        ),
    ]
