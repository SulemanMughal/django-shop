# Generated by Django 3.1.14 on 2022-09-19 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20220919_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='first name'),
        ),
    ]
