from django.urls import path
from . import views

urlpatterns = [
	path('authenticate/', views.authenticate, name="authenticate"),
	path('follow/<int:id>', views.follow, name="follow"),
	path('unfollow/<int:id>', views.unfollow, name="unfollow"),
	path('user/', views.user, name="user"),
	path('posts/', views.posts, name="posts"),
	path('posts/<int:id>', views.deletePost, name="deletePost"),
	path('like/<int:id>', views.like, name="like"),
	path('unlike/<int:id>', views.unlike, name="unlike"),
	path('comment/<int:id>', views.comment, name="comment"),
	path('getpost/<int:id>', views.getpost, name="getpost"),
	path('allpost/', views.allpost, name="allposts"),
]