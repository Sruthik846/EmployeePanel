from django.db import models    

class EmployeeDetails(models.Model):
    if_id = models.IntegerField(default = None,primary_key=True)
    empname = models.CharField(max_length=50 , null=True)
    emailid = models.CharField(max_length=50, null=True)
    mobileNo = models.CharField(max_length=10, null=True)
    password = models.CharField(max_length=20, null=True)
    unread_msg = models.BooleanField(default=True)
