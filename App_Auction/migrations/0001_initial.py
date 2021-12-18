# Generated by Django 3.2.10 on 2021-12-18 02:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_bidder', models.CharField(blank=True, max_length=100, null=True)),
                ('product_name', models.CharField(max_length=200)),
                ('product_photo', models.ImageField(upload_to='product_image')),
                ('minimum_bid_price', models.PositiveIntegerField()),
                ('selling_price', models.PositiveIntegerField(blank=True, null=True)),
                ('product_description', models.TextField()),
                ('auction_end_date', models.DateField()),
                ('status', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductLastPrices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('bidder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_Auction.productmodel')),
            ],
        ),
    ]
