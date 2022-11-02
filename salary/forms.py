from django import forms
from django.forms import  ModelForm
from .models import GrandTotal, SalaryDetails,specialIncome,Deductions



class salaryform(ModelForm):
    grade = forms.CharField(widget=forms.TextInput)
    attendance = forms.CharField(widget=forms.TextInput)
    salary = forms.CharField(widget=forms.TextInput)
    training_salary = forms.CharField(widget=forms.TextInput)
    bonus = forms.CharField(widget=forms.TextInput)
    night_shift = forms.CharField(widget=forms.TextInput)
    rent = forms.CharField(widget=forms.TextInput)
    other = forms.CharField(widget=forms.TextInput)
    total_salary = forms.CharField(widget=forms.TextInput)
    total_other_income = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = SalaryDetails
        fields = ['grade','attendance','salary','training_salary',
                 'bonus','night_shift','rent','other','total_salary',
                 'total_other_income'
                ]
    def clean(self):
        super(salaryform,self).clean()        
        return self.cleaned_data


class specialIncomeForm(ModelForm):
    HRA = forms.CharField(widget=forms.TextInput)
    invest_profit = forms.CharField(widget=forms.TextInput)
    Rsg_settlement = forms.CharField(widget=forms.TextInput)
    minimum_wage = forms.CharField(widget=forms.TextInput)
    from_last_month = forms.CharField(widget=forms.TextInput)
    festival_bonus = forms.CharField(widget=forms.TextInput)
    savings = forms.CharField(widget=forms.TextInput)
    total = forms.CharField(widget=forms.TextInput)
    survey_scheme = forms.CharField(widget=forms.TextInput)
    class Meta:
        model = specialIncome
        fields = ['HRA','invest_profit','Rsg_settlement','minimum_wage','survey_scheme',
                 'from_last_month','festival_bonus','savings','total',
                ]
    def clean(self):
        super(specialIncomeForm,self).clean()        
        return self.cleaned_data
        
class deductionForm(ModelForm):
    class Meta:
        model = Deductions
        fields = ['to_next_month','other','total']

class GR_Total_Form(ModelForm):
    total = forms.CharField(widget=forms.TextInput)
    class Meta:
        model = GrandTotal
        fields = ['total']
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total'].widget.attrs.update({'size':'10'})
        self.fields['total'].widget.attrs['style']  = 'border:1px solid;'

class Basic_Total_Form(ModelForm):
    total_salary = forms.CharField(widget=forms.TextInput)
    class Meta:
        model = SalaryDetails
        fields = ['total_salary']
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['total_salary'].widget.attrs.update({'size':'10'})
        self.fields['total_salary'].widget.attrs['style']  = 'border:1px solid;'
