from celery import shared_task

from accounts.models import Account
from shared.utils import create_thumbnails


@shared_task
def create_profile_thumbnail(account_id: str):
    create_thumbnails(account_id, Account, "profile")
