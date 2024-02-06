from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PostCard(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=100, blank=True)
    body = models.TextField(blank=True, null=True)
    image = models.URLField()
    date = models.DateField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def default_title(self):
        try:
            default_title = f"post-{PostCard.objects.last().id + 1}"
        except AttributeError:
            default_title = f"post-1"

        return default_title

    def save(self, *args, **kwargs):
        if not self.pk and not self.title:
            self.title = self.default_title()
        super().save(*args, **kwargs)

    view_name = 'view_name'

    def get_absolute_url(self):
        return reverse(viewname=self.view_name, kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class PhotoCard(PostCard):
    def default_title(self):
        try:
            default_title = f"photo-{PhotoCard.objects.last().id + 1}"
        except AttributeError:
            default_title = f"photo-1"

        return default_title

    view_name = 'photo-details'


class VideoCard(PostCard):
    def default_title(self):
        try:
            default_title = f"video-{VideoCard.objects.last().id + 1}"
        except AttributeError:
            default_title = f"video-1"

        return default_title

    view_name = 'video-details'


class VoiceCard(PostCard):
    def default_title(self):
        try:
            default_title = f"voice-{VoiceCard.objects.last().id + 1}"
        except AttributeError:
            default_title = f"voice-1"

        return default_title

    view_name = 'voice-details'


class ChatCard(PostCard):
    def default_title(self):
        try:
            default_title = f"chat-{ChatCard.objects.last().id + 1}"
        except AttributeError:
            default_title = f"chat-1"

        return default_title

    view_name = 'chat-details'
