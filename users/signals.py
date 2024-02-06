from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Token
from .views import get_new_token


@receiver(signal=post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        source_token = Token.objects.get(id=1)
        try:
            new_token = get_new_token(source_token.refresh_token)
            access_token = new_token['access_token']
            refresh_token = new_token['refresh_token']
        except KeyError:
            error_value = "Bad request: 'Generate Access Token' API!"
            access_token = error_value
            refresh_token = error_value
        Token.objects.create(
            access_token=access_token,
            refresh_token=refresh_token,
            user=instance
        )


@receiver(signal=post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.token.save()
