# Generated by Django 5.0.2 on 2024-03-22 23:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0003_course_val'),
        ('group', '0004_group_continuity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('parents', models.TextField()),
                ('coming', models.CharField(blank=True, max_length=255, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=11)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('no_started', 'Not Started'), ('continues', 'Continues'), ('completed', 'Completed'), ('deleted', 'Deleted')], default='no_started', max_length=20)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lids', to='course.course')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lids', to='group.group')),
            ],
            options={
                'ordering': ['fullname', '-update_time'],
            },
        ),
    ]
