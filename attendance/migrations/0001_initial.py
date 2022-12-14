# Generated by Django 3.2.8 on 2022-08-26 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonthData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=50, null=True)),
                ('year', models.CharField(choices=[('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')], max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PunchingDatas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ifid', models.IntegerField(default=None, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=50, null=True)),
                ('year', models.CharField(choices=[('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')], max_length=50, null=True)),
                ('WFO_attendance', models.FloatField(default=None, null=True)),
                ('OT_attendance', models.FloatField(default=None, null=True)),
                ('WFH_attendance', models.FloatField(default=None, null=True)),
                ('Punching_Mistake', models.FloatField(default=None, null=True)),
                ('Night_shift', models.FloatField(default=None, null=True)),
                ('Deduction', models.FloatField(default=None, null=True)),
                ('total_Attendance', models.FloatField(default=None, null=True)),
                ('date_1', models.CharField(default=None, max_length=255, null=True)),
                ('date_2', models.CharField(default=None, max_length=255, null=True)),
                ('date_3', models.CharField(default=None, max_length=255, null=True)),
                ('date_4', models.CharField(default=None, max_length=255, null=True)),
                ('date_5', models.CharField(default=None, max_length=255, null=True)),
                ('date_6', models.CharField(default=None, max_length=255, null=True)),
                ('date_7', models.CharField(default=None, max_length=255, null=True)),
                ('date_8', models.CharField(default=None, max_length=255, null=True)),
                ('date_9', models.CharField(default=None, max_length=255, null=True)),
                ('date_10', models.CharField(default=None, max_length=255, null=True)),
                ('date_11', models.CharField(default=None, max_length=255, null=True)),
                ('date_12', models.CharField(default=None, max_length=255, null=True)),
                ('date_13', models.CharField(default=None, max_length=255, null=True)),
                ('date_14', models.CharField(default=None, max_length=255, null=True)),
                ('date_15', models.CharField(default=None, max_length=255, null=True)),
                ('date_16', models.CharField(default=None, max_length=255, null=True)),
                ('date_17', models.CharField(default=None, max_length=255, null=True)),
                ('date_18', models.CharField(default=None, max_length=255, null=True)),
                ('date_19', models.CharField(default=None, max_length=255, null=True)),
                ('date_20', models.CharField(default=None, max_length=255, null=True)),
                ('date_21', models.CharField(default=None, max_length=255, null=True)),
                ('date_22', models.CharField(default=None, max_length=255, null=True)),
                ('date_23', models.CharField(default=None, max_length=255, null=True)),
                ('date_24', models.CharField(default=None, max_length=255, null=True)),
                ('date_25', models.CharField(default=None, max_length=255, null=True)),
                ('date_26', models.CharField(default=None, max_length=255, null=True)),
                ('date_27', models.CharField(default=None, max_length=255, null=True)),
                ('date_28', models.CharField(default=None, max_length=255, null=True)),
                ('date_29', models.CharField(default=None, max_length=255, null=True)),
                ('date_30', models.CharField(default=None, max_length=255, null=True)),
                ('date_31', models.CharField(default=None, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PunchingFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(choices=[('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')], max_length=50, null=True, verbose_name='Enter Year')),
                ('Month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=50, null=True, verbose_name='Enter Month')),
                ('file', models.FileField(upload_to='PunchData')),
                ('startdate', models.IntegerField(default=None, null=True)),
                ('enddate', models.IntegerField(default=None, null=True)),
            ],
        ),
    ]
