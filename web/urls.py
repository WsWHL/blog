from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^(?:index)?/?$', views.index, name='index'),
    path('login/', views.login, name='account'),
    path('register/', views.register, name='account'),
    path('code/', views.captcha_code, name='code'),
]
