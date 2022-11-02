from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    empid = forms.IntegerField( widget=(forms.NumberInput(attrs={'class': 'signup__input','autofocus': True,'placeholder':'IFID'})))
    username = forms.CharField(  widget=(forms.TextInput(attrs={'class': 'signup__input','placeholder':'Username'})))
    email = forms.CharField(  widget=(forms.TextInput(attrs={'class': 'signup__input','placeholder':'Email'})))
    mobileNo = forms.IntegerField(  widget=(forms.NumberInput(attrs={'class': 'signup__input','placeholder':'Mobile'})))
    password1 = forms.CharField(  widget=(forms.PasswordInput(attrs={'class': 'signup__input','placeholder':'Password'})))
    password2 = forms.CharField(  widget=(forms.PasswordInput(attrs={'class': 'signup__input','placeholder':'Re-enter Passsword'})))
    
    
    class Meta:
        model = User
        fields = ['empid','username','mobileNo','email','password1','password2']
    
    def clean(self):
        super(SignUpForm,self).clean()
        # extract mobile Number
        mobileNo = self.cleaned_data.get('mobileNo')
        if len(str(mobileNo))!=10:
            self._errors['mobileNo'] = self.error_class([
                'Mobile Number Should be 10 digits'])
        return self.cleaned_data