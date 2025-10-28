from django.urls import path
from . import views

urlpatterns = [
    path('get-all/', views.adverts_list, name='adverts_list'),
    path('add/', views.advert_create, name='advert_create'),
    path('info/<int:advert_id>/', views.advert_detail, name='advert_detail'),
]