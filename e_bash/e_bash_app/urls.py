from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('register/', views.reg, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('item/<int:id>', views.item_template, name='item')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)