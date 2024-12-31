# from django.urls import path
# from blogs import views


# urlpatterns = [
#     path('categories/', views.CategoryList.as_view(), name='category_list'),
#     path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category_detail'),
#     path('categories/create/', views.CategoryCreate.as_view(), name='category_create'),
#     path('categories/<int:pk>/update/', views.CategoryUpdate.as_view(), name='category_update'),
#     path('categories/<int:pk>/delete/', views.CategoryDelete.as_view(), name='category_delete'),

#     path('tags/', views.TagList.as_view(), name='tag_list'),
#     path('tags/<int:pk>/', views.TagDetail.as_view(), name='tag_detail'),
#     path('tags/create/', views.TagCreate.as_view(), name='tag_create'),
#     path('tags/<int:pk>/update/', views.TagUpdate.as_view(), name='tag_update'),

#     path('posts/', views.PostList.as_view(), name='post_list'),
#     path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
#     path('posts/create/', views.PostCreate.as_view(), name='post_create'),
#     path('posts/<int:pk>/update/', views.PostUpdate.as_view(), name='post_update'),
#     path('posts/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
# ]