# Generated by Django 4.1.6 on 2023-03-01 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Conference_data', '0011_alter_conference_conf_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='checked',
            field=models.BooleanField(default=False, verbose_name='Проверено'),
        ),
    ]
