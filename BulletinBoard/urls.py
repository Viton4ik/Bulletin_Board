
from django.urls import path

from .views import AdvertList, AdvertDetail, AdvertSearch, AdvertCreate, html_404, AdvertUpdate, AdvertDelete, ResponseList, ResponseDetail, ResponseDelete


urlpatterns = [
   path('', AdvertList.as_view(), name='advert_list'), 
   path('search/', AdvertSearch.as_view(), name='advert_search'), 
   path('<int:id>', AdvertDetail.as_view(), name='advert_detail'), 
   path('create/', AdvertCreate.as_view(), name='advert_create'),
   path('<int:pk>/edit/', AdvertUpdate.as_view(), name='advert_edit'),
   path('<int:pk>/delete/', AdvertDelete.as_view(), name='advert_delete'),
   path('responses', ResponseList.as_view(), name='response_list'), 
   path('responses/<int:pk>', ResponseDetail.as_view(), name='response_detail'), #FIXME: delete
   path('responses/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
   # path('create/', advert_create, name='advert_create'),
   path('404/', html_404, name='404'),
   
]
