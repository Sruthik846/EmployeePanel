from django.db import models

class salaryMonth(models.Model):
    months = (  ('January','January'),('February','February'),('March','March'),('April','April'),
                ('May','May'),('June','June'),('July','July'),('August','August'),
                ('September','September'),('October','October'),('November','November'),('December','December')
            )
    years = (   ('2018','2018'),('2019','2019'),('2020','2020'),
                ('2021','2021'),('2022','2022'),('2023','2023'),('2024','2024')
            )
    month = models.CharField(max_length=50,choices=months , null=True)
    year = models.CharField(max_length=50,choices=years , null=True)


class SalaryFile(models.Model):
    months = (  ('January','January'),('February','February'),('March','March'),('April','April'),
                ('May','May'),('June','June'),('July','July'),('August','August'),
                ('September','September'),('October','October'),('November','November'),('December','December')
            )
    years = (   ('2019','2019'),('2020','2020'),('2021','2021'),('2022','2022'),
                ('2023','2023'),('2024','2024'),('2025','2025'),
            )
    year = models.CharField("Enter Year", max_length=50 ,choices=years , null=True)  
    month  = models.CharField("Enter Month", max_length = 50 , choices=months , null=True)  
    file = models.FileField(upload_to='salary_data')

    def delete(self,*args,**kwargs):
        self.file.delete()
        super().delete(*args,**kwargs)

class SalaryDetails(models.Model):
    months = (  ('January','January'),('February','February'),('March','March'),('April','April'),
                ('May','May'),('June','June'),('July','July'),('August','August'),
                ('September','September'),('October','October'),('November','November'),('December','December')
            )
    years = (   ('2018','2018'),('2019','2019'),('2020','2020'),
                ('2021','2021'),('2022','2022'),('2023','2023'),('2024','2024')
            )
    ifid = models.IntegerField(default = None , null=True)
    name = models.CharField(max_length=50 , null=True)
    month = models.CharField(max_length=50,choices=months , null=True)
    year = models.CharField(max_length=50,choices=years , null=True)

    grade = models.CharField(max_length=20, null=True) 
    attendance = models.FloatField(default= None, null=True)
    salary = models.IntegerField(default= None, null=True)
    training_att = models.FloatField(default= None, null=True)
    training_salary = models.IntegerField(default= None, null=True)
    bonus = models.IntegerField(default= None, null=True)
    night_shift = models.FloatField(default= None, null=True)
    rent = models.IntegerField(default= None, null=True)
    other = models.FloatField(default= None, null=True)
    total_salary = models.IntegerField(default= None, null=True)
    total_other_income = models.IntegerField()

class specialIncome(models.Model):
    basicSalary = models.ForeignKey (SalaryDetails, default=None, on_delete=models.CASCADE)
    HRA = models.FloatField(default= None, null=True)
    invest_profit = models.FloatField(default= None, null=True)
    Rsg_settlement = models.FloatField(default= None, null=True)
    minimum_wage = models.FloatField(default= None, null=True)
    survey_scheme = models.FloatField(default= None, null=True)
    from_last_month = models.FloatField(default= None, null=True)
    festival_bonus = models.FloatField(default= None, null=True)
    savings = models.FloatField(default= None, null=True)
    total = models.FloatField(default= None, null=True)

class Deductions(models.Model):
    basicSalary = models.ForeignKey (SalaryDetails, default=None, on_delete=models.CASCADE)
    to_next_month = models.FloatField(default= None, null=True)
    other = models.FloatField(default= None, null=True)
    total = models.FloatField(default= None, null=True)

class GrandTotal(models.Model):
    basicSalary = models.ForeignKey (SalaryDetails, default=None, on_delete=models.CASCADE)
    total = models.FloatField(default= None, null=True)