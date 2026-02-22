from django.urls import path
from .views import RegisterView, UserProfileView

urlpatterns = [
    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/profile/', UserProfileView.as_view(), name='profile'),
]