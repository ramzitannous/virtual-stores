from django.db import migrations, models
import users.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='UUID identify', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=users.models.upload_location),
        ),
    ]
