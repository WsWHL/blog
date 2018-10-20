from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
                  re_path(r'^(?:index)?/?$', views.index, name='index'),
                  path('login/', views.user_login, name='account'),
                  path('register/', views.user_register, name='account'),
                  path('logout/', views.user_logout, name='logout'),
                  path('code/', views.captcha_code, name='code'),
                  path('article/', views.article, name='article'),
                  path('article/<int:article_id>/', views.article, name='article_id'),
                  path('upload/', views.upload, name='upload'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
