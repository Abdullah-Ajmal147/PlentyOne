# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=UserProfile)
def activate_user(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        if not user.is_active:
            user.is_active = True
            user.save()
