from django.urls import path, include
from . import views

urlpatterns = [
    path('token', views.TokenView.as_view()),
    path('user', views.UserView.as_view())
]
