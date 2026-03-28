from django.urls import path
from .views import CommentListCreateView, PostListByCategoryView, PostListCreateView, PostDetailView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('posts/category/<int:category_id>/', PostListByCategoryView.as_view(), name='post-list-by-category'),
]