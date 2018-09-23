from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^(?:index)?/?$', views.index, name='index'),
    path('login/', views.user_login, name='account'),
    path('register/', views.user_register, name='account'),
    path('logout/', views.user_logout, name='logout'),
    path('code/', views.captcha_code, name='code'),
]
