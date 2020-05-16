from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .forms import AccountChangeForm, AccountCreationForm
from .models import Account


class AccountAdmin(UserAdmin):
    add_form = AccountCreationForm
    list_filter = ("is_staff", "type", "status", "is_active", "on_trial")
    form = AccountChangeForm
    model = Account
    fieldsets = (
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "image")}),
        (_("Permissions"), {
            "fields": ("is_active", "is_staff", "is_superuser"),
        }),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        ("Account Status", {"fields": ("type", "status", "on_trial")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff",
                       "is_active", "image", "status", "type", "on_trial")}
        ),
    )
    list_display = ("image", "email", "is_staff", "status", "type", "on_trial")
    list_display_links = ("email", )
    search_fields = ("email",)
    ordering = ("email",)
    actions = ("force_delete", )

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

    def force_delete(self, request, queryset):
        queryset.delete()

    force_delete.short_description = "Force Delete User"


admin.site.register(Account, AccountAdmin)
