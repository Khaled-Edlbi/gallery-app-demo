from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),

    path('photos/', photos, name='photos'),
    path('photos/create/', PhotoCreateView.as_view(), name='photo-create'),
    path('photos/<int:pk>/', PhotoDetailView.as_view(), name='photo-details'),
    path('photos/<int:pk>/edit/', PhotoEditView.as_view(), name='photo-edit'),
    path('photos/<int:pk>/delete/', PhotoDeleteView.as_view(), name='photo-delete'),

    path('videos/', videos, name='videos'),
    path('videos/create/', VideoCreateView.as_view(), name='videos-create'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-details'),
    path('videos/<int:pk>/edit/', VideoEditView.as_view(), name='videos-edit'),
    path('videos/<int:pk>/delete/', VideoDeleteView.as_view(), name='videos-delete'),

    path('voices/', voices, name='voices'),
    path('voices/create/', VoiceCreateView.as_view(), name='voices-create'),
    path('voices/<int:pk>/', VoiceDetailView.as_view(), name='voice-details'),
    path('voices/<int:pk>/edit/', VoiceEditView.as_view(), name='voices-edit'),
    path('voices/<int:pk>/delete/', VoiceDeleteView.as_view(), name='voices-delete'),

    path('chats/', chats, name='chats'),
    path('chats/create/', ChatCreateView.as_view(), name='chats-create'),
    path('chats/<int:pk>/', ChatDetailView.as_view(), name='chat-details'),
    path('chats/<int:pk>/edit/', ChatEditView.as_view(), name='chats-edit'),
    path('chats/<int:pk>/delete/', ChatDeleteView.as_view(), name='chats-delete'),

    path('post-type/', select_post_type, name='select-post-type')
]
