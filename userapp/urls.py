from django.urls import path
from .views import UserAPIView,RegisterAPIView

urlpatterns = [
    path('userapi/', UserAPIView.as_view(), name='user-list'),
    path('userapi/<int:pk>/', UserAPIView.as_view(), name='user-detail'),
    path('userapi/<int:pk>/delete/', UserAPIView.as_view(), name='user-delete'),
    path('register/', RegisterAPIView.as_view(), name='register-user'),

]