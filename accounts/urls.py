from django.urls import path
from .views import SignUp, logout_view


urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('logout/', logout_view, name='logout')
]