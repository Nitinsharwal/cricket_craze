from django.urls import path
from . import views

urlpatterns = [
    path('', views.cricket_data_view, name='cricket_data'),
    path('players/', views.player_info_view, name='player_info'),
    path('matches/', views.match_info_view, name='match_info'),
    path('match/<str:id>/', views.match_detail_view, name='match_detail'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact, name='contact'),
    path('<id>/', views.default_url, name='default_url'),
]
