# Generated by Django 3.2.18 on 2023-03-13 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0004_alter_table_payment_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientsubscription',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='clientsubscription', to='subscriptions.subscription'),
        ),
    ]