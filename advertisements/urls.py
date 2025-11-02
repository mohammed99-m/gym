from django.urls import path
from . import views
from .views import AdvertisementListApi , AdvertisementListCreateAPIView

urlpatterns = [
    ##path('get-all/', views.adverts_list, name='adverts_list'),
    ##path('add/', views.advert_create, name='advert_create'),
    path('info/<int:advert_id>/', views.advert_detail, name='advert_detail'),

    path('get_all_advertisment/',AdvertisementListApi.as_view(),name="get_all_advertisment"),
    path('create-advert/',AdvertisementListCreateAPIView.as_view(),name="add_advertisment")
]

# curl -X POST "http://mohammedgym22.pythonanywhere.com/advertisements/create-advert/" ^
#   -H "Accept: application/json" ^
#   -F "title=Super Promo22" ^
#   -F "content=50% off this month" ^
#   -F "is_active=true" ^
#   -F "image=@C:\Users\mwe33\Desktop\pexels-photo-2261484.jpeg"

# curl -X POST "http://mohammedgym22.pythonanywhere.com/advertisements/create-advert/" ^
# -H "Accept: application/json" ^
# -F "title=Super Promo22" ^
# -F "content=50% off this month" ^
# -F "is_active=true" ^
# -F "image=@C:/Users/mwe33/Desktop/pexels-photo-2261484.jpeg"


# curl -X POST "http://mohammedgym22.pythonanywhere.com/advertisements/create-advert/" ^
#   -H "Accept: application/json" ^
#   -F "title=Super Promo22" ^
#   -F "content=50% off this month" ^
#   -F "is_active=true" ^
#   -F "image=@C:/Users/mwe33/Desktop/pexels-photo-2261484.jpeg"
