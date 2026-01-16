from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('register/', views.reg, name='register'),
    path('logout/', views.logout_view, name='logout'),
]