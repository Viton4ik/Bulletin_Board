
from django.urls import path

from .views import AdvertList, AdvertDetail, AdvertSearch, AdvertCreate, html_404, AdvertUpdate, \
   AdvertDelete, ResponseList, ResponseDelete, ResponseCreate, ResponseList_ad, ResponseList_in, ResponseList_ad_in, \
      ResponseUpdate 


urlpatterns = [
   path('', AdvertList.as_view(), name='advert_list'), 
   path('search/', AdvertSearch.as_view(), name='advert_search'), 
   path('<int:id>', AdvertDetail.as_view(), name='advert_detail'), 
   path('create/', AdvertCreate.as_view(), name='advert_create'),
   path('<int:pk>/edit/', AdvertUpdate.as_view(), name='advert_edit'),
   path('<int:pk>/delete/', AdvertDelete.as_view(), name='advert_delete'),
   path('responses', ResponseList.as_view(), name='response_list'), 
   path('responses_in', ResponseList_in.as_view(), name='response_list_in'), 
   path('<int:pk>/responses', ResponseList_ad.as_view(), name='response_list_ad'), 
   path('<int:pk>/responses_in', ResponseList_ad_in.as_view(), name='response_list_ad_in'), 
   path('responses/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
   path('<int:pk>/responses/create/', ResponseCreate.as_view(), name='response_create'),
   path('responses/<int:pk>/accepted', ResponseUpdate.as_view(), name='accepted'),
   path('404/', html_404, name='404'),
   
]
