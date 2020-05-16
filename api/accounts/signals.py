from django.dispatch import receiver
from django.db.models import signals
from .tasks import create_account_profile
from accounts.models import Account


@receiver(signals.post_save, sender=Account)
def create_profile_image(sender, instance: Account, created, **kwargs):
    create_account_profile.delay(str(instance.id))