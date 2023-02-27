# Generated by Django 4.1.6 on 2023-02-23 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Conference_data', '0010_alter_conference_conf_date_begin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='conf_address',
            field=models.TextField(blank=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='conf_card_href',
            field=models.URLField(blank=True, max_length=500, verbose_name='Карточка конференции'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='conf_date_begin',
            field=models.DateField(blank=True, null=True, verbose_name='Дата начала'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='conf_date_end',
            field=models.DateField(blank=True, null=True, verbose_name='Дата окончания'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='conf_desc',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='conf_href',
            field=models.URLField(blank=True, max_length=500, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='conf_name',
            field=models.TextField(blank=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='conf_s_desc',
            field=models.TextField(blank=True, verbose_name='Краткое описание'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='contacts',
            field=models.TextField(blank=True, verbose_name='Контакты'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='org_name',
            field=models.TextField(blank=True, verbose_name='Организатор'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='reg_date_begin',
            field=models.DateField(blank=True, null=True, verbose_name='Начало регистрации'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='reg_date_end',
            field=models.DateField(blank=True, null=True, verbose_name='Окончание регистрации'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='reg_href',
            field=models.URLField(blank=True, max_length=500, verbose_name='Ссылка на регистрацию'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='rinc',
            field=models.BooleanField(verbose_name='РИНЦ'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='tags',
            field=models.ManyToManyField(blank=True, to='Conference_data.tag', verbose_name='Теги'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='themes',
            field=models.TextField(blank=True, verbose_name='Тематика (от организатора)'),
        ),
        migrations.AlterField(
            model_name='conference',
            name='un_name',
            field=models.CharField(max_length=500, verbose_name='ВУЗ'),
        ),
    ]
