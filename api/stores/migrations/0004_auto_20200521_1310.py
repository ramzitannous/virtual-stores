from django.db import migrations
import shared.fields
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0003_auto_20200517_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='image_ppoi',
            field=versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20),
        ),
        migrations.AlterField(
            model_name='store',
            name='image',
            field=shared.fields.Base64ThumbnailField(null=True, upload_to=''),
        ),
    ]
