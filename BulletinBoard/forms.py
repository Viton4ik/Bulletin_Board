
from django import forms

from .models import Advert#, Response


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

# class ResponseForm(forms.ModelForm):
#     # accepted = forms.FileField(widget=forms.CheckboxSelectMultiple()) 
#     class Meta:

#         model = Response
#         fields = [
#                   'accepted',
#               ]
#         widgets = {
#             'accepted': forms.CheckboxSelectMultiple(),
#         }

