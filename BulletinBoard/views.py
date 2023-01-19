
from django.shortcuts import render
from django.views.generic import ListView, DetailView#, UpdateView, DeleteView, CreateView

# add models
from .models import Advert, Category, Response

#FIXME: to be deleted later
from pprint import pprint


class AdvertList(ListView):
    model = Advert
    ordering = '-createTime'
    template_name = 'BulletinBoard/advert_list.html'
    context_object_name = 'adverts'


class AdvertDetail(DetailView):
    model = Advert
    template_name = 'BulletinBoard/advert.html'
    context_object_name = 'advert'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.get_object().upload:
            context['if_picture'] = self.get_object().if_picture()
            context['get_extention'] = self.get_object().get_file_name().split('.')[-1]


        # to get info in console
        pprint(context)
        print(f"self.object:{self.object}")
        print(f"**kwargs:{kwargs}")
        print(f"**self.kwargs:{self.kwargs}")

        return context


