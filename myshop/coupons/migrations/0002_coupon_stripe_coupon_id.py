# Generated by Django 3.1.14 on 2022-09-18 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='stripe_coupon_id',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]