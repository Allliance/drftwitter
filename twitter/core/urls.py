from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.UserView.as_view(), name='index')
]
