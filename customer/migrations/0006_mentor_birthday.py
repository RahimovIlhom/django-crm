# Generated by Django 5.0.2 on 2024-03-18 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_student_coming'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]