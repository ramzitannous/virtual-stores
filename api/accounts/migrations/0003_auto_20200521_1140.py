from django.db import migrations
import shared.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200518_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='image',
            field=shared.fields.Base64ThumbnailField(blank=True, null=True, upload_to='profile', verbose_name='Image'),
        ),
    ]
