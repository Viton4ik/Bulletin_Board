
from django.urls import path

from .views import AdvertList, AdvertDetail


urlpatterns = [
   path('', AdvertList.as_view(), name='advert_list'), 
   path('<int:id>', AdvertDetail.as_view(), name='advert_detail'), 

]
