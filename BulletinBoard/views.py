
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
# from django.core.files.storage import FileSystemStorage

from .filters import AdvertFilter#, ResponseFilter

from .forms import AdvertForm, ResponseForm, ResponseFormAccept

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
        
        # #TODO
        # context['response_id'] = Response.objects.filter(author=self.request.user.id).values_list('id', flat=True)

        pprint(context)
        print(f"**kwargs:{self.kwargs}")
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

# responses list view received by user
class ResponseList_in(ListView):
    model = Response
    ordering = '-createTime'
    template_name = 'BulletinBoard/response_list_in.html'
    context_object_name = 'responses_in'
    paginate_by = 8

    def get_queryset(self):
        """ get filter: Received responses """
        self.advert__author = get_object_or_404(User, id=self.request.user.id)
        if self.request.GET:
            try:
                if self.request.GET['accepted_button'] == "True":
                    queryset = Response.objects.filter(advert__author=self.advert__author, accepted=True).order_by('-createTime')
                elif self.request.GET['accepted_button'] == "False":
                    queryset = Response.objects.filter(advert__author=self.advert__author, accepted=False).order_by('-createTime')
            except:
                queryset = Response.objects.filter(advert__author=self.advert__author).order_by('-createTime')
        else:
            queryset = Response.objects.filter(advert__author=self.advert__author).order_by('-createTime')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get filter: Received responses 
        if self.request.GET:
            try:
                if self.request.GET['accepted_button'] == "True":
                    context['search_result'] = len(Response.objects.filter(advert__author=self.request.user.id, accepted=True))
                elif self.request.GET['accepted_button'] == "False":
                    context['search_result'] = len(Response.objects.filter(advert__author=self.request.user.id, accepted=False))
            except:
                context['search_result'] = len(Response.objects.filter(advert__author=self.request.user.id))
        else:
            context['search_result'] = len(Response.objects.filter(advert__author=self.request.user.id))

        context['GET'] = self.request.GET
        context['user_'] = self.request.user.username

        # Filter -> to get user responses list only
        context['user_responses'] = Response.objects.filter(author=self.request.user.id)
               
        # # Filter -> to get user responses list releted to the specific advert - is not used!!!
        # advert_filter = {}
        # for message in Response.objects.filter(author=self.request.user.id):
        #     qs = Response.objects.filter(author=self.request.user.id, advert=message.advert.id).order_by('-createTime')#.values_list('text',flat=True)
        #     advert_filter[message.advert] = qs
        # context['advert_filter'] = advert_filter

        # to get info in console
        pprint(context)
        
        return context
        

# responses list view sent by user
class ResponseList(ListView):
    # form_class = ResponseForm
    model = Response
    ordering = '-createTime'
    template_name = 'BulletinBoard/response_list.html'
    context_object_name = 'responses'
    paginate_by = 8

    def get_queryset(self):
        """ get filter: only self.user responses releted to advert"""
        self.author = get_object_or_404(User, id=self.request.user.id)
        if self.request.GET:
            try:
                if self.request.GET['accepted_button'] == "True":
                    queryset = Response.objects.filter(author=self.author, accepted=True).order_by('-createTime')
                elif self.request.GET['accepted_button'] == "False":
                    queryset = Response.objects.filter(author=self.author, accepted=False).order_by('-createTime')
            except:
                queryset = Response.objects.filter(author=self.author).order_by('-createTime')
        else:
            queryset = Response.objects.filter(author=self.author).order_by('-createTime')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get filter: sent responses 
        if self.request.GET:
            try:
                if self.request.GET['accepted_button'] == "True":
                    context['search_result'] = len(Response.objects.filter(author=self.author, accepted=True))
                elif self.request.GET['accepted_button'] == "False":
                    context['search_result'] = len(Response.objects.filter(author=self.author, accepted=False))
            except:
                context['search_result'] = len(Response.objects.filter(author=self.author))
        else:
            context['search_result'] = len(Response.objects.filter(author=self.author))

        context['GET'] = self.request.GET
        context['user_'] = self.request.user.username

        # Filter -> to get user responses list only
        context['user_responses'] = Response.objects.filter(author=self.request.user.id)
               
        # to get info in console
        pprint(context)
        
        return context


# sent responses connected to the specific advert
class ResponseList_ad(ListView):
    model = Response
    ordering = '-createTime'
    template_name = 'BulletinBoard/response_list_ad.html'
    context_object_name = 'responses_ad'
    paginate_by = 8

    def get_queryset(self):
        """ get filter: only self.user responses releted to advert"""
        self.advert = get_object_or_404(Advert, id=self.kwargs['pk'])
        self.author = get_object_or_404(User, id=self.request.user.id)
        queryset = Response.objects.filter(advert=self.advert, author=self.author).order_by('-createTime')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_'] = self.request.user.username
        context['advert_'] = Advert.objects.get(id=self.kwargs['pk'])

        # to get info in console
        pprint(context)
        print(f"**kwargs:{self.kwargs}")
        return context


# received responses connected to the specific advert
class ResponseList_ad_in(ListView):
    model = Response
    ordering = '-createTime'
    template_name = 'BulletinBoard/response_list_ad_in.html'
    context_object_name = 'responses_ad_in'
    paginate_by = 8

    def get_queryset(self):
        """ get filter: Received responses """
        self.advert = get_object_or_404(Advert, id=self.kwargs['pk'])
        self.author = get_object_or_404(User, id=self.request.user.id)
        queryset = Response.objects.filter(advert=self.advert, advert__author=self.author).order_by('-createTime')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_'] = self.request.user.username
        context['advert_'] = Advert.objects.get(id=self.kwargs['pk'])

        # to get info in console
        pprint(context)
        print(f"**kwargs:{self.kwargs}")
        return context


class ResponseCreate(CreateView):
    form_class = ResponseForm
    model = Response
    template_name = 'BulletinBoard/response_create.html'
    success_url = reverse_lazy('response_list')

    def form_valid(self, form):
        text = form.save(commit=False)
        text.text = self.request.POST['text']

        advert = form.save(commit=False)
        advert.advert = Advert.objects.get(id=self.kwargs['pk'])
        
        # get user. if None -> 404
        author = form.save(commit=False)
        if self.request.user.username:
            author.author = User.objects.get(username=self.request.user.username)
        else:
            return HttpResponseRedirect('../../../404/')  

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advert_title'] = Advert.objects.get(id=self.kwargs['pk'])

        pprint(context)
        # print(f"**kwargs:{self.kwargs['pk']}")

        return context


class ResponseDelete(DeleteView): 
    model = Response
    template_name = 'BulletinBoard/response_delete.html'
    success_url = reverse_lazy('response_list')


class ResponseUpdate(UpdateView): #class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = ResponseFormAccept
    model = Response
    template_name = 'BulletinBoard/accepted.html'
    success_url = reverse_lazy('response_list_in')


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