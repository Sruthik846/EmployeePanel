from django import forms
from django.forms import ModelForm
from .models import *

class credforms(ModelForm):
    class Meta:
        model = EmployeeMobile
        fields = "__all__"

    def clean(self):
        super(credforms,self).clean()
        # extract mobile Number
        mobileNo = self.cleaned_data.get('mobile')
        if len(str(mobileNo))!=10:
            self._errors['mobile'] = self.error_class([
                'Mobile Number Should be 10 digits'])
        if EmployeeMobile.objects.filter(mobile=mobileNo).exists():
            self._errors['mobile'] = self.error_class([
                'Mobile Number already Exists'])
        ifid = self.cleaned_data.get('ifid')
        if EmployeeMobile.objects.filter(ifid=ifid).exists():
            self._errors['ifid'] = self.error_class([
                'IFID already Exists'])
        return self.cleaned_data

class updateCred(ModelForm):
    class Meta:
        model = EmployeeMobile
        fields = "__all__"