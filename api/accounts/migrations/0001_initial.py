import accounts.enums
import accounts.models
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUID identify', primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to=accounts.models.upload_location)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('type', models.CharField(choices=[(accounts.enums.AccountTypes['NORMAL'], accounts.enums.AccountTypes['NORMAL']), (accounts.enums.AccountTypes['BUSINESS'], accounts.enums.AccountTypes['BUSINESS'])], default=accounts.enums.AccountTypes['NORMAL'], max_length=10)),
                ('status', models.CharField(choices=[(accounts.enums.AccountStatus['VERIFIED'], accounts.enums.AccountStatus['VERIFIED']), (accounts.enums.AccountStatus['UN_VERIFIED'], accounts.enums.AccountStatus['UN_VERIFIED']), (accounts.enums.AccountStatus['PENDING'], accounts.enums.AccountStatus['PENDING'])], default=accounts.enums.AccountStatus['UN_VERIFIED'], max_length=20)),
                ('on_trial', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
