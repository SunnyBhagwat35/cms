# Generated by Django 4.2.9 on 2024-01-14 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cmsuser",
            name="phone",
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name="cmsuser",
            name="pincode",
            field=models.CharField(max_length=6),
        ),
    ]