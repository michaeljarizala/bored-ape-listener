# Generated by Django 5.1.1 on 2024-10-09 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_id', models.CharField(max_length=42)),
                ('sender', models.CharField(max_length=42)),
                ('recipient', models.CharField(max_length=42)),
                ('trn_hash', models.CharField(max_length=64, unique=True)),
                ('block_no', models.IntegerField()),
            ],
        ),
    ]
