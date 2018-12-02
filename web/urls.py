from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
                  re_path(r'^(?:index)?/?$', views.index, name='index'),
                  path('index/p<int:pager>/', views.index, name='index_pager'),
                  path('index/u<int:user_id>/', views.index, name='user_index'),
                  path('index/u<int:user_id>/p<int:pager>/', views.index, name='user_blog_pager'),
                  path('login/', views.user_login, name='account'),
                  path('register/', views.user_register, name='account'),
                  path('logout/', views.user_logout, name='logout'),
                  path('code/', views.captcha_code, name='code'),
                  path('article/', views.article, name='article'),
                  path('article/<int:article_id>/', views.article, name='article_id'),
                  path('upload/', views.upload, name='upload'),
                  path('reading/<int:article_id>/', views.reading, name='reading'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
