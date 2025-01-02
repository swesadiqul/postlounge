from django.urls import path
from blogs import views


urlpatterns = [
    path('categories/', views.CategoryView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/<int:pk>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('tags/create/', views.TagCreateView.as_view(), name='tag_create'),
    path('tags/<int:pk>/update/', views.TagUpdateView.as_view(), name='tag_update'),
    path('tags/<int:pk>/delete/', views.TagDeleteView.as_view(), name='tag_delete'),

    # path('posts/', views.PostList.as_view(), name='post_list'),
    # path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    # path('posts/create/', views.PostCreate.as_view(), name='post_create'),
    # path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='post_update'),
    # path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
]