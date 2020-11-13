from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from accounts.enums import Gender


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


def get_extra_info(backend, user, response, *args, **kwargs):
    if backend.name == "facebook":
        gender = response["gender"]
        return {
            "gender": Gender.M if gender == "male" else gender.F,
        }
    else:
        return {
            "gender": Gender.M
        }


def save_image(backend, user, response, *args, **kwargs):
    from accounts.tasks import save_social_image
    save_social_image.delay(str(user.id), backend.name, response)
