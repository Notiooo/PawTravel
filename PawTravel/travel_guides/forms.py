from tinymce.widgets import TinyMCE

from .models import Guide
from django import forms

class GuideForm(forms.ModelForm):
    '''
    Form for creating new travel guides
    '''
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 40, 'rows': 30}))
    category=forms.ChoiceField(choices=Guide.CATEGORY_CHOICES, required=True)
    country=forms.ChoiceField(choices=Guide.COUNTRY_CHOICES, required=True)



    class Meta:
        model=Guide
        fields=('title', 'description', 'body', 'category', 'country')