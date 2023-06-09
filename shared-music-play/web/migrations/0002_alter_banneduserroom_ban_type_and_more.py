# Generated by Django 4.1.4 on 2023-06-05 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="banneduserroom",
            name="ban_type",
            field=models.CharField(
                choices=[("room", "Бан в комнате"), ("chat", "Бан в чате")], default="room", max_length=15
            ),
        ),
        migrations.AlterField(
            model_name="banneduserroom",
            name="banned_until",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(default="username", max_length=255),
            preserve_default=False,
        ),
    ]
