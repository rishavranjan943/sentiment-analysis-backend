# api/urls.py
from django.urls import path
from .views import RegisterView, LoginView, MoodView, MoodHistoryView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('mood/', MoodView.as_view(), name='mood'),
    path('moods/history/', MoodHistoryView.as_view(), name='mood_history'),
]
