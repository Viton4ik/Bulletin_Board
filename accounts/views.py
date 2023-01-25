from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

from .forms import SignUpForm

class SignUp(CreateView):
    model = User
    form_class = SignUpForm

    # URL, на которой нужно направить пользователя после успешной обработки формы;
    success_url = '/accounts/login'

    template_name = 'registration/signup.html'


def logout_view(request):
    logout(request)