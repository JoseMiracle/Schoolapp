# Generated by Django 4.0.5 on 2022-10-03 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mySchoolapp', '0022_assignmentsolution_number_of_submission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentsolution',
            name='score',
            field=models.IntegerField(null=True),
        ),
    ]