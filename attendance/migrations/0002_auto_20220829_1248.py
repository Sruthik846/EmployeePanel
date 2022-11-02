# Generated by Django 3.2.8 on 2022-08-29 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='punchingfile',
            name='enddate',
        ),
        migrations.RemoveField(
            model_name='punchingfile',
            name='startdate',
        ),
        migrations.AddField(
            model_name='punchingdatas',
            name='file',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.punchingfile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='punchingfile',
            name='file',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]