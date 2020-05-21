from django.dispatch import receiver
from django.db.models import signals
from accounts.models import Account
from accounts.tasks import create_profile_thumbnail


@receiver(signals.post_save, sender=Account)
def receive_account_created(sender, instance: Account, created, **kwargs):
    create_profile_thumbnail.delay(str(instance.id))
