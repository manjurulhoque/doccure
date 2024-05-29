# Generated by Django 5.0.6 on 2024-05-29 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doctors", "0004_auto_20210327_0811"),
    ]

    operations = [
        migrations.AddField(
            model_name="experience",
            name="designation",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="experience",
            name="working_here",
            field=models.BooleanField(
                default=False, verbose_name="Currently working here"
            ),
        ),
    ]