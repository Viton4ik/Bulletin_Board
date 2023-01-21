
from django.urls import path

from .views import AdvertList, AdvertDetail, AdvertSearch, AdvertCreate# advert_create


urlpatterns = [
   path('', AdvertList.as_view(), name='advert_list'), 
   path('search/', AdvertSearch.as_view(), name='advert_search'), 
   path('<int:id>', AdvertDetail.as_view(), name='advert_detail'), 
   path('create/', AdvertCreate.as_view(), name='advert_create'),
   # path('create/', advert_create, name='advert_create'),
   
]
