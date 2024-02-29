# Generated by Django 5.0 on 2024-01-07 08:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("django_app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="postratings",
            name="count",
        ),
        migrations.AddField(
            model_name="post",
            name="slug",
            field=models.SlugField(default="changeit"),
        ),
        migrations.AlterField(
            model_name="resume",
            name="photo",
            field=models.ImageField(
                blank=True,
                default=None,
                null=True,
                upload_to="hr/requests/photos",
                verbose_name="Изображение",
            ),
        ),
    ]