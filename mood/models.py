# api/models.py
from django.db import models
from django.contrib.auth.models import User

class Mood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.TextField()
    sentiment = models.CharField(max_length=10)  # Positive, Negative, Neutral
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood}"
