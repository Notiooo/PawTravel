from tinymce.widgets import TinyMCE

from .models import Guide, GuideCategory, Country
from django import forms


class GuideForm(forms.ModelForm):
    """
    Form for creating new travel guides
    """
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 40, 'rows': 30}))
    category = forms.ChoiceField(
        widget=forms.Select,
        choices=(),
        required=True
    )

    country = forms.ChoiceField(
        widget=forms.Select,
        choices=(),
        required=True
    )

    class Meta:
        model = Guide
        fields = ('title', 'description', 'body', 'category', 'country', 'image')

    def __init__(self, *args, **kwargs):
        """
        Loads the countries and categories available for selection into the form
        """
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [(category.id, category.name) for category in GuideCategory.objects.all()]
        self.fields['country'].choices = [(country.id, country.name) for country in Country.objects.all()]
