# Generated by Django 5.1.4 on 2025-01-02 11:29

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_discountcode_cart_discount_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
