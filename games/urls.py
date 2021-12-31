from django.urls import path
from . import views

urlpatterns = [
    path('match', views.MatchView.as_view()),
    path('submission', views.SubmissonView.as_view()),
]