# Generated by Django 4.0.5 on 2022-09-05 08:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mySchoolapp', '0009_remove_subjectfile_subject_topics_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectfile',
            name='subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mySchoolapp.subjects'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateTimeField(default=datetime.date(2022, 9, 4)),
        ),
    ]
