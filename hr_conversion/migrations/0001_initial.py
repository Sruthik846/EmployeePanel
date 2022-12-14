# Generated by Django 3.2.8 on 2022-08-26 04:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_file', models.FileField(upload_to='conversion/emp')),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ifid', models.IntegerField(default=None, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('designation', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='punchingXL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('punching_files', models.FileField(upload_to='conversion')),
            ],
        ),
    ]
