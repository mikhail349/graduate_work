# Generated by Django 3.2.18 on 2023-03-12 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_alter_table_clients'),
        ('subscriptions', '0003_auto_20230306_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.client'),
        ),
    ]
