
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Name")
    last_name = forms.CharField(label="Last Name")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


# customised form
# from allauth.account.forms import SignupForm, UserForm, PasswordField, BaseSignupForm
# from django.contrib.auth.models import Group


# class CustomSignupForm(SignupForm):

#     def save(self, request):
#         user = super().save(request)
#         common_users = Group.objects.get(name="common users")
#         user.groups.add(common_users)
#         return user