# Generated by Django 4.1.6 on 2023-03-26 18:38

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Conference_data', '0003_alter_conference_conf_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='conf_s_desc',
            field=ckeditor.fields.RichTextField(blank=True, default=None, null=True, verbose_name='Краткое описание'),
        ),
    ]
