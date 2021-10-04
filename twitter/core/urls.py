from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.UserView.as_view(), name='user'),
    path('twit/<int:pk>', views.TwitDetailView.as_view(), name='view_twit'),
    path('twit/', views.NewTwitView.as_view(), name='twit'),
    path('comment/<int:pk>', views.CommentView.as_view(), name='comment'),
]
