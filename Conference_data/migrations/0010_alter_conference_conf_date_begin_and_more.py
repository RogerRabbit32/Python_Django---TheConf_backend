# Generated by Django 4.1.6 on 2023-02-23 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Conference_data', '0009_alter_conference_conf_date_begin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='conf_date_begin',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conference',
            name='conf_date_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conference',
            name='reg_date_begin',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conference',
            name='reg_date_end',
            field=models.DateField(blank=True, null=True),
        ),
    ]
