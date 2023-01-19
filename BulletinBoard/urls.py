
from django.urls import path

from .views import AdvertList, AdvertDetail, AdvertSearch


urlpatterns = [
   path('', AdvertList.as_view(), name='advert_list'), 
   path('search/', AdvertSearch.as_view(), name='advert_search'), 
   path('<int:id>', AdvertDetail.as_view(), name='advert_detail'), 
   
]
