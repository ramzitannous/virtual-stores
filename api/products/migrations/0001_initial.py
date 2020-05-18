from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import products.enum
import uuid
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stores', '0003_auto_20200517_0741'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUID identify', primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=' category', verbose_name='Image')),
                ('image_ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20)),
                ('parent', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUID identify', primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('discount_price', models.IntegerField(default=None, null=True)),
                ('on_discount', models.BooleanField(default=False)),
                ('colors', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), default=list, size=None)),
                ('sizes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=5), choices=[(products.enum.ProductSize['XS'], products.enum.ProductSize['XS']), (products.enum.ProductSize['S'], products.enum.ProductSize['S']), (products.enum.ProductSize['M'], products.enum.ProductSize['M']), (products.enum.ProductSize['L'], products.enum.ProductSize['L']), (products.enum.ProductSize['XL'], products.enum.ProductSize['XL']), (products.enum.ProductSize['XXL'], products.enum.ProductSize['XXL'])], default=list, size=None)),
                ('integer_sizes', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(45)]), default=list, size=None)),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('is_active', models.BooleanField(default=True)),
                ('extras', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.Category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL)),
                ('store', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='stores.Store')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUID identify', primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=400)),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='products.Product')),
            ],
            options={
                'verbose_name_plural': 'Product Reviews',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUID identify', primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='product', verbose_name='Image')),
                ('image_ppoi', versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.Product')),
            ],
            options={
                'verbose_name_plural': 'Product Images',
            },
        ),
    ]
