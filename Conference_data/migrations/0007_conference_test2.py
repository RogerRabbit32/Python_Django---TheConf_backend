# Generated by Django 4.1.6 on 2023-04-16 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Conference_data', '0006_conference_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='test2',
            field=models.CharField(default='', max_length=100),
        ),
    ]
