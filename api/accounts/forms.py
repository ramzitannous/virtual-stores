from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Account


class AccountCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Account
        fields = ('email', 'first_name', "last_name", 'image',
                  "status", "type", "on_trial")


class AccountChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ('email', 'image', "status", "type", "on_trial")
