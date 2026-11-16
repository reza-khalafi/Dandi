from django.urls import path
from apps.articles.views import HomeView, ArticleDetailView, ArticleSearchView

app_name = 'articles'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('articles/api/feed/', ArticleSearchView.as_view(), name='api_feed'),
    path('article/<str:slug>/', ArticleDetailView.as_view(), name='detail'),
]
