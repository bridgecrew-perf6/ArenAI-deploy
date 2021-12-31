from django.urls import path
from . import views

urlpatterns = [
    path('env', views.BotEnvView.as_view()),
    path('bot', views.BotItemView.as_view()),
    path('all-bot', views.BotAllView.as_view()),
    path('bot-file', views.BotDownloadView.as_view()),

]