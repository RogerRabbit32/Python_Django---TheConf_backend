# Generated by Django 4.1.6 on 2023-04-16 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Conference_data', '0005_conference_generate_conf_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='test',
            field=models.BooleanField(default=False),
        ),
    ]