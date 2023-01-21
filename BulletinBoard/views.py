
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView#, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

from .filters import AdvertFilter

from .forms import AdvertForm

from .models import Advert, Category, Response

from django.urls import reverse_lazy


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
        context['total'] = len(self.filterset.qs)

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
        #TODO: delete
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


class AdvertCreate(CreateView):
    form_class = AdvertForm
    model = Advert
    template_name = 'BulletinBoard/advert_edit.html'
    # success_url = reverse_lazy('advert_list')

    def get_success_url(self):
        """ 
        Provides using app/forms.py with redirect if post-form completed
        """
        return reverse_lazy('advert_detail', kwargs={'id': self.object.id})

    def form_valid(self, form):
        contentType = form.save(commit=False)
        contentType.contentType = 'advert'

        # TODO: activate this and delete author in forms.py in templates
        author = form.save(commit=False)
        author.author = User.objects.get(username=self.request.user.username)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['category_list'] = Category.objects.all().values_list('text', flat=True)
        # context['author'] = self.request.user.username
        return context

# def advert_create(request):
#     if request.method == 'POST':
#         form = AdvertForm(request.POST, request.FILES)
#         author = form.save(commit=False)
#         author.author = User.objects.get(username=request.user.username)
#         if form.is_valid():

#             form.save()
#             return HttpResponseRedirect('../') 
#     else:
#         form = AdvertForm

#     return render(request, 'BulletinBoard/advert_edit.html', {'form':form})

# def create_post(request):
#     if request.method == 'POST':
#         form = AdvertForm(request.POST, request.FILES)
#         files = request.FILES.getlist('file') #field name in model
#         if form.is_valid():# and file_form.is_valid():
#             form.save()
#             return HttpResponseRedirect("/") 
#     else:
#         form = AdvertForm
#     return render(request, 'BulletinBoard/advert_edit.html', {'form':form})