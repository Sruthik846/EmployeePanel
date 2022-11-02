from django.db import models

class MonthData(models.Model):
    months = (  ('January','January'),('February','February'),('March','March'),('April','April'),
                ('May','May'),('June','June'),('July','July'),('August','August'),
                ('September','September'),('October','October'),('November','November'),('December','December')
            )
    years = (   ('2018','2018'),('2019','2019'),('2020','2020'),
                ('2021','2021'),('2022','2022'),('2023','2023'),('2024','2024')
            )
    month = models.CharField(max_length=50,choices=months , null=True)
    year = models.CharField(max_length=50,choices=years , null=True)


class PunchingFile(models.Model):
    
    months = (  ('January','January'),('February','February'),('March','March'),('April','April'),
                ('May','May'),('June','June'),('July','July'),('August','August'),
                ('September','September'),('October','October'),('November','November'),('December','December')
            )
    years = (   ('2018','2018'),('2019','2019'),('2020','2020'),
                ('2021','2021'),('2022','2022'),('2023','2023'),('2024','2024')
            )
    year = models.CharField("Enter Year", max_length=50 ,choices=years , null=True)  
    Month  = models.CharField("Enter Month", max_length = 50 , choices=months , null=True)  
    file = models.CharField(max_length=50 ,default= None,null=True)
    
    def delete(self,*args,**kwargs):
        self.file.delete()
        super().delete(*args,**kwargs)

class PunchingDatas(models.Model):
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

    WFO_attendance = models.FloatField(default= None, null=True)
    OT_attendance = models.FloatField(default=None ,null=True)
    WFH_attendance = models.FloatField(default=None ,null=True)
    Punching_Mistake = models.FloatField(default=None ,null=True)
    Night_shift = models.FloatField(default=None ,null=True)
    Deduction = models.FloatField(default=None ,null=True)
    total_Attendance = models.FloatField(default=None ,null=True)
    # Relation ---> PunchFile
    file = models.ForeignKey (PunchingFile,on_delete=models.CASCADE)

for dt in range(1,32):
    PunchingDatas.add_to_class("date_"+str(dt), models.CharField(max_length=255 ,default=None, null=True))