
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse_lazy

from django.http import HttpResponseRedirect

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django.conf import settings

from django.core.mail import send_mail

from .filters import AdvertFilter

from .forms import AdvertForm, ResponseForm, ResponseFormAccept

from .models import Advert, Response

from datetime import datetime

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
        
        pprint(context)
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


class AdvertCreate(LoginRequiredMixin, CreateView):
    # 403.html
    raise_exception = True

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
 

class AdvertUpdate(LoginRequiredMixin, UpdateView): 
    """
    'get_absolute_url' function in models is used -> 'get_success_url' is not used here
    """
    # 403.html
    raise_exception = True

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


class AdvertDelete(LoginRequiredMixin, DeleteView): 
    # 403.html
    raise_exception = True

    model = Advert
    template_name = 'BulletinBoard/advert_delete.html'
    success_url = reverse_lazy('advert_list')

# ===== Advetr views =====


# ===== Response views =====

# responses list view received by user
class ResponseList_in(LoginRequiredMixin, ListView):
    # 403.html
    raise_exception = True

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
               
        # to get info in console
        pprint(context)
        return context
        

# responses list view sent by user
class ResponseList(LoginRequiredMixin, ListView):
    # 403.html
    raise_exception = True

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
class ResponseList_ad(LoginRequiredMixin, ListView):
    # 403.html
    raise_exception = True

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
class ResponseList_ad_in(LoginRequiredMixin, ListView):
    # 403.html
    raise_exception = True

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


class ResponseCreate(LoginRequiredMixin, CreateView):
    # 403.html
    raise_exception = True

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
        print(f"**kwargs:{self.kwargs['pk']}")
        return context


class ResponseDelete(LoginRequiredMixin, DeleteView): 
    # 403.html
    raise_exception = True

    model = Response
    template_name = 'BulletinBoard/response_delete.html'
    success_url = reverse_lazy('response_list')


# Accepted view
class ResponseUpdate(LoginRequiredMixin, UpdateView): 
    # 403.html
    raise_exception = True

    form_class = ResponseFormAccept
    model = Response
    template_name = 'BulletinBoard/accepted.html'
    success_url = reverse_lazy('response_list_in')

    def form_valid(self, form):
        """ send a email if response is accepted"""
        if User.objects.filter(id=self.request.user.id):
            user_ = User.objects.get(id=self.request.user.id)
            user_response_ = Response.objects.get(id=self.kwargs['pk']).author
            advert_ = Response.objects.get(id=self.kwargs['pk']).advert
            response_ = Response.objects.get(id=self.kwargs['pk'])
            send_mail(
                subject=f'Acception message!' ,
                message=f'MMORPG portal greetings you! \nResponse "{response_.text}" for advert "{advert_.title}" has been accepted by "{user_.username}"!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_response_.email, user_.email]
            )
        else:
            return HttpResponseRedirect('404')  
        return super().form_valid(form)

# ===== Response views =====
