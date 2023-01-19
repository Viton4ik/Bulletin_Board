
from django import forms

from .models import Advert


class AdvertForm(forms.ModelForm):

    class Meta:

        model = Advert

        fields = [
                  'author',
                  'title',
                  'text',
                  'category',
                  'upload',
              ]

    # widgets = {
    #     'author': forms.HiddenInput(),
    # }
    # def clean(self):
    #     cleaned_data = super().clean()
    #     topic = cleaned_data.get("topic")
    #     if topic is not None and len(topic) < 5:
    #         raise ValidationError({
    #             "topic": "Описание не может быть менее 5 символов."
    #         })
    #     content = cleaned_data.get("content")
    #     if content == topic:
    #         raise ValidationError(
    #             "Content and topic are the same. Please correct!"
    #         )

    #     return cleaned_data

