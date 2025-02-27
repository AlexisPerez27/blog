from django.urls import path 
from .views import PostListView, PostDetails, PostHeadingView, IncrementPostClicView


urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/', PostDetails.as_view(), name='post-detail'),
    path('posts/heading/', PostHeadingView.as_view(), name='post-heading'),
    path('posts/<slug>/increment_clicks/', IncrementPostClicView.as_view(), name='increment-post-click')
]