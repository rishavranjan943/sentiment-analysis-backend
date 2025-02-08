# api/views.py
from rest_framework import serializers, views, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Mood
from rest_framework.permissions import IsAuthenticated
from textblob import TextBlob



# Register View
class RegisterView(views.APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return Response({'error': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)

# Login View
class LoginView(views.APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Mood View (Track Mood and Perform Sentiment Analysis)
class MoodView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        mood_text = request.data.get('mood')
        user = request.user
        if mood_text:
            # Sentiment analysis
            blob = TextBlob(mood_text)
            sentiment = 'Positive' if blob.sentiment.polarity > 0 else 'Negative' if blob.sentiment.polarity < 0 else 'Neutral'
            
            # Save Mood to database
            mood = Mood.objects.create(user=user, mood=mood_text, sentiment=sentiment)
            return Response(serializers.MoodSerializer(mood).data, status=status.HTTP_201_CREATED)
        return Response({'error': 'No mood text provided'}, status=status.HTTP_400_BAD_REQUEST)

# Mood History View
class MoodHistoryView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        moods = Mood.objects.filter(user=request.user).order_by('-timestamp')
        return Response(serializers.MoodSerializer(moods, many=True).data)
