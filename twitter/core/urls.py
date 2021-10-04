from django.urls import path
from . import views

urlpatterns = [
    path('user', views.UserView.as_view(), name='user'),
    path('user/<str:username>', views.UserTwitsView.as_view(), name='get_user_twits'),
    path('twit/', views.NewTwitView.as_view(), name='new_twit'),
    path('twit/<int:twit_id>', views.TwitDetailsView.as_view(), name='twit_details'),
    path('twit/<int:twit_id>/comment', views.CommentView.as_view(), name='comment'),
]
