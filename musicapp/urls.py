from django.urls import path
from .views import MusicAPIView,ArtistAPIView

urlpatterns = [
    path('musicapi/', MusicAPIView.as_view(), name='music-list'),
    path('musicapi/<int:pk>/', MusicAPIView.as_view(), name='music-detail'),
    path('artistapi/', ArtistAPIView.as_view(), name='artist-list'),
    path('artistapi/<int:pk>/', ArtistAPIView.as_view(), name='artist-detail'),
]