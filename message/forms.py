from django.forms import ModelForm,Textarea

from .models import IFMessages

class IFmessageForm(ModelForm):
    class Meta:
        model = IFMessages
        exclude = ('id','upload_date','updated_at','file')
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 20, 'height':100,'padding':2}),
        }
