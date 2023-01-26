from django.urls import path

from .views import logout_view, signin_view, account_confirmation#, SignUp


urlpatterns = [
    # path('signup/', SignUp.as_view(), name='signup'), # is not used
    path('logout/', logout_view, name='logout'),
    # add confirmation with a token
    path('signin/', signin_view, name="signin"),
    path('confirmation/', account_confirmation, name="confirm"),
]