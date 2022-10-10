from django.urls import path,re_path
from .views import (ArticleCreateView,ArticleDetailView,
         ArticleUpdateView,ArticleListView,
         ArticleCounterView,DeleteArticleView,
         HomeView, CategoryList,SearchView)
app_name="article"

urlpatterns = [
    path('',HomeView.as_view(),name='index'),
    path('list/',ArticleListView.as_view(),name="list"),
    path('redirect/<pk>/',ArticleCounterView.as_view(),name='redirect'),
    path('<int:pk>/',ArticleDetailView.as_view(), name='detail'),
    path('create/',ArticleCreateView.as_view(), name='create'),
    path('<pk>/update', ArticleUpdateView.as_view(),name="update"),
    path('<pk>/delete/',DeleteArticleView.as_view(),name='delete'),
    path('categories/<str:category>/',CategoryList.as_view(),name='category'),
    path('search/',SearchView.as_view(),name='search')
]