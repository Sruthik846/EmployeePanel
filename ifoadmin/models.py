from django.db import models

class EmployeeMobile(models.Model):
    ifid = models.IntegerField(default=None, primary_key=True)
    name = models.CharField(max_length=50 , null=True)
    mobile = models.CharField(max_length=10, null=True)


class CredFile(models.Model):
    xlfile = models.FileField(upload_to='credfiles') # for creating file input  
    
    def delete(self,*args,**kwargs):
        self.xlfile.delete()
        super().delete(*args,**kwargs)
