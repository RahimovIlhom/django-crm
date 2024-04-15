# Generated by Django 5.0.2 on 2024-03-30 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lid_app', '0002_lid_school'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('location', models.CharField(max_length=50)),
                ('was_answered', models.BooleanField(default=False)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
    ]