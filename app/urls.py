from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<slug:slug>', views.post_page, name='post_page'),
    path('tag/<slug:slug>', views.tag_page, name='tag_page'),
    path('author/<slug:slug>', views.author_page, name='author_page'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('accounts/register', views.register_user, name='register'),
    path('bookmark/<slug:slug>', views.bookmark, name='bookmark'),
    path('likes/<slug:slug>', views.likes, name='likes'),
    path('all_bookmarks/', views.all_bookmarks, name='all_bookmarks'),
    path('all_posts/', views.all_posts, name='all_posts'),
    path('all_likes/', views.all_likes, name='all_likes'),
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('unsubscribe/', views.unsubscribe_view, name='unsubscribe'),
    path('author/<slug:slug>/posts', views.author_all_post, name='author_all_post'),
    path('author/<slug:slug>/posts/create/', views.create_post, name='create_post'),
    path('author/<slug:slug>/posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('author/<slug:slug>/posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('author/<slug:slug>/edit', views.edit_profile, name='edit_profile'),

    

] 