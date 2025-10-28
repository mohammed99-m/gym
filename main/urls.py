from django.urls import path
from . import views

urlpatterns = [
    path('players/', views.get_players,name="get_all_players"),
    path('add-player/', views.add_player, name='add_player'),
    path('player/<str:player_id>/',views.get_player,name="get_player"),
    path('delete/<str:player_id>/',views.delete_player,name="delete_player"),
    path('login-player/', views.login_player, name='login_player'),
    path('update-player/<int:player_id>/', views.update_player, name='player_detail_or_delete')
]