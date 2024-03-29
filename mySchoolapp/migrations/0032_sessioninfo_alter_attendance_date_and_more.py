# Generated by Django 4.0.5 on 2022-10-11 03:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySchoolapp', '0031_alter_subjectfile_date_uploaded'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=9)),
                ('session_starts', models.DateTimeField()),
                ('session_ends', models.DateTimeField()),
                ('no_of_terms', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateTimeField(default=datetime.date(2022, 10, 10)),
        ),
        migrations.AlterField(
            model_name='subjectfile',
            name='date_uploaded',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 10, 16, 31, 54, 474363)),
        ),
    ]
