# Generated by Django 4.0.5 on 2022-09-05 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mySchoolapp', '0011_assignmentfiles_alter_attendance_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignmentfiles',
            old_name='subject_files',
            new_name='subject_assignment_files',
        ),
    ]