from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateTimeFilter
from django.forms import DateTimeInput
from django.contrib.auth.models import User

from .models import Advert, Category


class AdvertFilter(FilterSet):

    title = CharFilter(field_name='title',
                       lookup_expr='contains',
                       label='Title:',
                     )

    author = ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all(),
        label='User:',
        empty_label='any',
    )

    category = ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Category:',
        empty_label='any',
    )

    """ add time widget """
    createTime = DateTimeFilter(
        field_name='createTime',
        lookup_expr='gte',
        label='Creation date:',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M', # there is no reaction on this!
            attrs={'type': 'date'}, 
        ),
    )



