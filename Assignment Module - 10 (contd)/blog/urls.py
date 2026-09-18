from django.urls import path
from . import views

urlpatterns = [
    # Main
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('search/', views.search, name='search'),
    path('popular/', views.popular_posts, name='popular_posts'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Posts CRUD
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('my-posts/', views.my_posts, name='my_posts'),

    # Comments
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/reply/', views.add_reply, name='add_reply'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    # Likes
    path('post/<int:pk>/like/', views.toggle_post_like, name='toggle_post_like'),
    path('comment/<int:comment_id>/like/', views.toggle_comment_like, name='toggle_comment_like'),

    # Ratings
    path('post/<int:pk>/rate/', views.rate_post, name='rate_post'),

    # Profile
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
