from django.urls import path
from .views import UserAPIView

urlpatterns = [
    path('userapi/', UserAPIView.as_view(), name='user-list'),
    path('userapi/<int:pk>/', UserAPIView.as_view(), name='user-detail'),
]