from django.urls import path
from . import views

urlpatterns = [
    path('user/<int:pk>/', views.UserView.as_view(), name='user'),
    path('twit/<int:pk>/', views.TwitView.as_view(), name='twit'),
    path('comment/<int:pk>', views.CommentView.as_view(), name='comment'),
]
