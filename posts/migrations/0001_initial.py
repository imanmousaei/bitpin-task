# Generated by Django 5.1.4 on 2025-01-04 08:53

import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=63, verbose_name='Article Title')),
                ('text', models.TextField(max_length=1023, verbose_name='Article text')),
                ('rate_count', models.PositiveBigIntegerField(default=0, verbose_name='Number of ratings for this post')),
                ('average_rating', models.DecimalField(decimal_places=3, default=Decimal('0'), max_digits=6, verbose_name='Average Rating for this post')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveSmallIntegerField(choices=[(0, 'Shit'), (1, 'Very Poor'), (2, 'Poor'), (3, 'Neutral'), (4, 'Good'), (5, 'Excellent')])),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customers.customer')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
            options={
                'unique_together': {('customer', 'post')},
            },
        ),
    ]
