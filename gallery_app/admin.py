from django.contrib import admin
from .models import PhotoCard, VideoCard, VoiceCard, ChatCard


admin.site.register(PhotoCard)
admin.site.register(VideoCard)
admin.site.register(VoiceCard)
admin.site.register(ChatCard)
