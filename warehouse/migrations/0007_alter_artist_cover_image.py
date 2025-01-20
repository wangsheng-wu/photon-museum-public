# Generated by Django 5.1.4 on 2024-12-15 04:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("warehouse", "0006_alter_artist_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artist",
            name="cover_image",
            field=models.ImageField(
                blank=True,
                default="artist_covers/placeholder.jpg",
                null=True,
                upload_to="artist_covers/",
            ),
        ),
    ]
