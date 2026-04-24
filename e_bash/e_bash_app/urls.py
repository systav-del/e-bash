from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    
    #Страница авторизации
    path('auth/', views.auth, name='auth'), # name - это имя маршрута

    #Страница регистрации
    path('reg/', views.reg, name='reg'),

    path('logout/', views.logout_view, name='logout'),

    path('items/<str:clothing_type>', views.items_list, name='items_list'),

    path('item/<int:id>', views.item_template, name='item'),

    path('account/', views.account, name='account')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)