# Generated by Django 5.0 on 2023-12-08 08:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crud_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owned_product', to='crud_user.user')),
                ('users_favorite', models.ManyToManyField(related_name='favorite_products', to='crud_user.user')),
            ],
        ),
    ]
