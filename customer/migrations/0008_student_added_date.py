# Generated by Django 5.0.2 on 2024-04-03 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_student_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='added_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
