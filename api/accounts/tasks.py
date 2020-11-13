from io import BytesIO
from celery import shared_task
from accounts.models import Account
from shared.session import get_requests_session
from shared.utils import create_thumbnails


@shared_task
def create_profile_thumbnail(account_id: str):
    create_thumbnails(account_id, Account, "profile")


@shared_task
def save_social_image(account_id: str, backend_name: str, response: dict):
    if backend_name == "facebook":
        image_url = f"http://graph.facebook.com/{response['id']}/picture?type=large"
    else:
        image_url = response["picture"]
    account = Account.objects.get(id=account_id)
    request_session = get_requests_session()
    with request_session as req:
        response = req.get(image_url)
    response.raise_for_status()
    img_fp = BytesIO(response.content)
    account.image.save(f"{account_id}.png", img_fp)
    account.save()
    create_thumbnails(account_id, Account, "profile")
