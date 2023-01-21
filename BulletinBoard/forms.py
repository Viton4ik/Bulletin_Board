
from django import forms

from .models import Advert


class AdvertForm(forms.ModelForm):
    # file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True})) 
    class Meta:

        model = Advert
        fields = [
                  'title',
                  'text',
                  'category',
                  'upload',
              ]
        widgets = {
            'upload': forms.ClearableFileInput(attrs={'multiple': True}),
        }



