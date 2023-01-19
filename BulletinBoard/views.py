
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView#, UpdateView, DeleteView
from django.contrib.auth.models import User

from .filters import AdvertFilter
# from .forms import AdvertForm

from .models import Advert, Category, Response

# from datetime import datetime

#FIXME: to be deleted later
from pprint import pprint


class AdvertList(ListView):
    model = Advert
    ordering = '-createTime'
    template_name = 'BulletinBoard/advert_list.html'
    context_object_name = 'adverts'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdvertFilter(self.request.GET, queryset)
        pprint(self.filterset)  # to get info in console
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset

        # to get info in console
        pprint(context)
        
        return context


class AdvertDetail(DetailView):
    model = Advert
    template_name = 'BulletinBoard/advert.html'
    context_object_name = 'advert'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # check if upload file is a picture
        if self.get_object().upload:
            context['if_picture'] = self.get_object().if_picture()
            context['get_extention'] = self.get_object().get_file_name().split('.')[-1]

        # to get info in console
        pprint(context)
        print(f"self.object:{self.object}")
        print(f"**kwargs:{kwargs}")
        print(f"**self.kwargs:{self.kwargs}")

        return context


class AdvertSearch(ListView):
    model = Advert
    ordering = '-createTime'
    template_name = 'BulletinBoard/advert_search.html'
    context_object_name = 'adverts'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdvertFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['search_result'] = len(self.filterset.qs)

        pprint(context)
        return context


# class AdvertCreate(CreateView):
#     form_class = AdvertForm
#     model = Advert
#     template_name = 'BulletinBoard/advert_edit.html'

#     # переопределяем метод form_valid и устанавливаем поле модели равным 'post'.
#     # Далее super().form_valid(form) запустит стандартный механизм сохранения, который вызовет form.save(commit=True)
#     def form_valid(self, form):
#         contentType = form.save(commit=False)
#         contentType.contentType = 'news'
#         return super().form_valid(form)
