# Generated by Django 3.1.1 on 2020-09-09 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]