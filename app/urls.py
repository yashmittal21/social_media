from django.urls import path
from . import views

urlpatterns = [
	path('authenticate/', views.authenticate, name="authenticate"),
	path('follow/<int:id>', views.follow, name="follow"),
]