# Generated by Django 4.1.7 on 2023-02-26 21:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscriptions', '0001_create_model_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='role_name',
            field=models.CharField(help_text='A role name from Auth Service', max_length=255),
        ),
        migrations.CreateModel(
            name='SubscriptionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.IntegerField(choices=[(1, 'Activate'), (2, 'Deactivate')])),
                ('event_dt', models.DateTimeField(auto_now_add=True)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='subscriptions.subscription')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
