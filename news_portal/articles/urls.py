from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('news/search/', views.search, name='news_search'),
    path('news/create/', views.create_news, name='create_news'),
    path('articles/create/', views.create_article, name='create_article'),
    path('articles/<int:pk>/delete/', views.delete_article, name='delete_article'),
    path('news/<int:pk>/delete/', views.delete_news, name='delete_news'),
    path('news/<int:pk>/edit/', views.edit_news, name='edit_news'),
    path('articles/<int:pk>/edit/', views.edit_article, name='edit_article'),
]
