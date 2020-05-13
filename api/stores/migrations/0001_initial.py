from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUID identify', primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(max_length=500)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('phone', models.CharField(max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('open_time', models.TimeField()),
                ('close_time', models.TimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StoreAddress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUID identify', primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('city', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('extra', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StoreReview',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUID identify', primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=400)),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.Store')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='store',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.StoreAddress'),
        ),
        migrations.AddField(
            model_name='store',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
