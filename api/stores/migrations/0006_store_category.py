from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20200521_1322'),
        ('stores', '0005_auto_20200525_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='products.Category'),
            preserve_default=False,
        ),
    ]
