from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_store_deactivate_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storereview',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='stores.Store'),
        ),
    ]
