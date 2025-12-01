from django.urls import path
from . import views

urlpatterns = [
    path('', views.aidat_listesi, name='aidat_listesi'), 
    path('ode/<int:aidat_id>/', views.aidat_ode, name='aidat_ode'), 
    path('borclandir/', views.toplu_borclandirma, name='toplu_borclandirma'),
    path('register/', views.register, name='register'), # <<< Yeni kayıt URL'si
]