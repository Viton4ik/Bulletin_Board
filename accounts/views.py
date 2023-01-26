
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User

from django.conf import settings

from django.views.generic.edit import CreateView

from django.shortcuts import render, redirect

from django.core.mail import send_mail

from .forms import SignUpForm, ConfirmationForm

from .models import Token

from random import randint


# is not used - url is deactivated!
class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'


def logout_view(request):
    logout(request)


def signin_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()                           # save user in DB
        user.refresh_from_db()                       # get this user again
        user.is_active = False                       # set the user as inactive
        user.save()                                  # save again

        # generate and create token
        generated_code = randint(1000, 9999)
        Token.objects.create(code=generated_code, user=user)

        # send it to the user
        send_mail(
            subject='Registration confirmation',
            message=f'To activate registration for user "{user.username}" please use this token: {generated_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[f'{user.email}']
        )
        return redirect('confirm')
    else:
        form = SignUpForm()
    return render(request, 'registration/signin.html', {'form': form})


def account_confirmation(request):
    form = ConfirmationForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['token']                                            # get a token put in by user
        user_ = form.cleaned_data['user']                                            # get a username put in by user
        if Token.objects.filter(code=code) and User.objects.filter(username=user_):  # check if the token and user exist in DB
            token_obj = Token.objects.get(code=code)                                 
            user_name_ = User.objects.get(username=user_).username                    # get username in DB
            user = token_obj.user                                                     # find the user related to the code
            if user.username == user_name_:
                user.is_active = True                                                 # activate the user
                user.save()                                                           # save
                login(                                                                # login him automatically
                    request, 
                    user, 
                    backend='django.contrib.auth.backends.ModelBackend'               # use authentication backend
                )   
                return redirect('/adverts')  
        else:
            form = ConfirmationForm()
            message = 'Incorrect data!'
    else:
        form = ConfirmationForm()
        message = ''
    return render(request, 'registration/account_confirmation.html', {'form': form, 'message': message})