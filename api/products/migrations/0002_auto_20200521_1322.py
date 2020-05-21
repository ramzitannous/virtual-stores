from django.db import migrations
import shared.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=shared.fields.Base64ThumbnailField(blank=True, null=True, upload_to='product', verbose_name='Image'),
        ),
    ]
