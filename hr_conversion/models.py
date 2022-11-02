from django.db import models
from django.utils import timezone

# Create your models here.
class punchingXL(models.Model):  
    punching_files   = models.FileField(upload_to='conversion') # for creating file input  
    
    def delete(self,*args,**kwargs):
        self.punching_files.delete()
        super().delete(*args,**kwargs)

class EmployeeFile(models.Model):
    employee_file = models.FileField(upload_to='conversion/emp') # for creating file input  
    upload_date = models.DateTimeField(default=timezone.now, null=True)
    def delete(self,*args,**kwargs):
        self.employee_file.delete()
        super().delete(*args,**kwargs)

class EmployeeList(models.Model):
    ifid = models.IntegerField(default = None , null=True)
    name = models.CharField(max_length=50 , null=True)
    designation = models.CharField(max_length=50 , null=True)