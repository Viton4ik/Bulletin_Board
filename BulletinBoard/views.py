
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

from .filters import AdvertFilter, ResponseFilter

from .forms import AdvertForm#, ResponseForm

from .models import Advert, Response

from django.urls import reverse_lazy

from datetime import datetime


#FIXME: to be deleted later
from pprint import pprint

# ===== service views =====

def html_404(request):
    form = AdvertForm()
    if not request.user.username:
        anonymous = 'User is not found'
    return render(request, 'BulletinBoard/404.html', {
        'form' : form,
        'anonymous': anonymous,
        })

# def html_403(request):
#     form = AdvertForm()
#     return render(request, '403.html', {'form' : form})

# ===== service views =====


# ===== Advetr views =====

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
        
        context['advert_author'] = self.get_object().author.username
        context['user_'] = self.request.user.username

        # if user_is_author
        context['user_is_author'] = context['user_'] == context['advert_author']
        
        #TODO
        context['response_id'] = Response.objects.filter(author=self.request.user.id).values_list('id', flat=True)

        pprint(context)
        print(f"self.object.id:{self.object.id}")

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
        return context


class AdvertCreate(CreateView):
    form_class = AdvertForm
    model = Advert
    template_name = 'BulletinBoard/advert_edit.html'
    # success_url = reverse_lazy('advert_list') # only if 'get_success_url' is not used

    def get_success_url(self):
        """ 
        Provides using app/forms.py with redirect if post-form completed
        Or we don't need it if 'get_absolute_url' function in models is used
        """
        return reverse_lazy('advert_detail', kwargs={'id': self.object.id})

    def form_valid(self, form):
        contentType = form.save(commit=False)
        contentType.contentType = 'advert'

        # get user. if None -> 404
        author = form.save(commit=False)
        if self.request.user.username:
            author.author = User.objects.get(username=self.request.user.username)
        else:
            return HttpResponseRedirect('../404/')  

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = 'Create'
        return context
 

class AdvertUpdate(UpdateView): 
    """
    'get_absolute_url' function in models is used -> 'get_success_url' is not used here
    """
    form_class = AdvertForm
    model = Advert
    template_name = 'BulletinBoard/advert_edit.html'

    # save last editing time for the post
    def form_valid(self, form):
        editTime = form.save(commit=False)
        editTime.editTime = datetime.now()

        # get user. if None -> 404
        author = form.save(commit=False)
        if self.request.user.username:
            author.author = User.objects.get(username=self.request.user.username)
        else:
            return HttpResponseRedirect('../404/')  

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = 'Edit'
        return context


class AdvertDelete(DeleteView): 
    model = Advert
    template_name = 'BulletinBoard/advert_delete.html'
    success_url = reverse_lazy('advert_list')

# ===== Advetr views =====


# ===== Response views =====

class ResponseList(ListView):
    # form_class = ResponseForm
    model = Response
    ordering = '-createTime'
    template_name = 'BulletinBoard/response_list.html'
    context_object_name = 'responses'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ResponseFilter(self.request.GET, queryset)
        pprint(self.filterset)  # to get info in console
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset.qs'] = self.filterset.qs
        context['filterset'] = self.filterset
        context['search_result'] = len(self.filterset.qs)
        context['user_'] = self.request.user.username
        
        
        # get user responses list releted to the specific advert
        advert_filter = {}
        for message in Response.objects.filter(author=self.request.user.id):
            qs = Response.objects.filter(author=self.request.user.id, advert=message.advert.id).order_by('-createTime')#.values_list('text',flat=True)
            advert_filter[message.advert] = qs
        context['advert_filter'] = advert_filter

        # to get info in console
        pprint(context)
        
        return context

#FIXME: delete with a template
class ResponseDetail(DetailView):
    model = Response
    template_name = 'BulletinBoard/response.html'
    context_object_name = 'response'
    # pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user_id_'] = self.request.user.id
        context['user_responses'] = Response.objects.filter(author=context['user_id_'])

        pprint(context)
        print(f"self.object.id:{self.object.id}")

        return context


class ResponseDelete(DeleteView): 
    model = Response
    template_name = 'BulletinBoard/response_delete.html'
    success_url = reverse_lazy('response_list')

# ===== Response views =====








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