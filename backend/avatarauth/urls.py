from django.contrib import admin
from django.urls import path

from . import views

app_name = 'avatarauth'
urlpatterns = [
    path('activate/<str:user_uuid>/', views.AvatarActivationView.as_view(), name='activate_avatar'),
]
