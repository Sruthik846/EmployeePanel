from django.db import models
from django.utils import timezone


# Create your models here.
class IFMessages(models.Model):
    title = models.CharField(max_length=50 , null=True)
    description = models.CharField(max_length=1000 , null=True)
    upload_date = models.DateTimeField(default=timezone.now, null=True)
    updated_at = models.DateTimeField(null=True,default=None,)

    
    def __str__(self):
        return self.title 

class msgFiles(models.Model):
    message = models.ForeignKey (IFMessages, default=None, on_delete=models.CASCADE)
    files = models.FileField(upload_to='messages/files')
    def __str__(self):
        return self.message.title 
    
    def delete(self,*args,**kwargs):
        self.files.delete()
        super().delete(*args,**kwargs)