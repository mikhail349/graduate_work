# Generated by Django 3.2.18 on 2023-03-05 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientsubscription',
            name='payment_system_subscription_id',
            field=models.CharField(max_length=255),
        ),
    ]