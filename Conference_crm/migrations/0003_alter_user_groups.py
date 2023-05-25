# Generated by Django 4.1.6 on 2023-05-23 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("Conference_crm", "0002_remove_user_group_alter_user_groups"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True, related_name="custom_users", to="auth.group"
            ),
        ),
    ]