from django.forms import ModelForm
from .models import *

class id_attendance(ModelForm):
    class Meta:
        model = PunchingDatas
        exclude =('id','month','year')