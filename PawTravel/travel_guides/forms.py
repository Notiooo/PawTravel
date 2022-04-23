from .models import Guide
from django import forms

class GuideForm(forms.ModelForm):
    '''
    Form for creating new travel guides
    '''

    class Meta:
        model=Guide
        fields=('title', 'description', 'category', 'country', 'body', 'author')