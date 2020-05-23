from accounts.enums import Gender
from django.db import migrations, models
import django.utils.timezone
import uuid
import accounts


def set_default_gender(apps, schema_editor):
    Account = apps.get_model('accounts', 'Account')
    for account in Account.objects.all().iterator():
        account.gender = Gender.M
        account.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200521_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountAddress',
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
        migrations.AddField(
            model_name='account',
            name='gender',
            field=models.CharField(choices=[(accounts.enums.Gender['M'], accounts.enums.Gender['M']), (accounts.enums.Gender['F'], accounts.enums.Gender['F'])], default=accounts.enums.Gender['F'], max_length=1),
            preserve_default=False
        ),
        migrations.RunPython(set_default_gender),
        migrations.AddField(
            model_name='account',
            name='address',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.AccountAddress'),
        ),
        migrations.AlterField(
            model_name='account',
            name='phone',
            field=models.CharField(max_length=100, unique=True),
        )
    ]
