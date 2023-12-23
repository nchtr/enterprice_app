# Generated by Django 5.0 on 2023-12-23 18:13

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Vacancies",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=250, verbose_name="naming")),
                ("description", models.TextField(verbose_name="desc")),
                ("company", models.CharField(max_length=100)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="hr/vacancies",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "date_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Дата и время создания",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=False, verbose_name="activity"),
                ),
                (
                    "is_distant",
                    models.BooleanField(default=False, verbose_name="worktype"),
                ),
                ("salary", models.IntegerField()),
            ],
            options={
                "verbose_name": "вакансии",
                "verbose_name_plural": "вакансии",
                "ordering": ("-date_time", "title"),
            },
        ),
        migrations.CreateModel(
            name="Messages",
            fields=[
                (
                    "message_id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="айди сообщения",
                    ),
                ),
                ("text", models.TextField(default="Пустое сообщение.")),
                (
                    "date_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Дата и время создания",
                    ),
                ),
                ("is_read", models.BooleanField(default=False)),
                (
                    "from_user",
                    models.OneToOneField(
                        default="Аноним",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sender",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "to_user",
                    models.OneToOneField(
                        default="Админ_нейм",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reciever",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "soobscheniya",
                "verbose_name_plural": "soobscheniya",
                "ordering": ("-message_id", "-date_time"),
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=300, verbose_name="Наименование"),
                ),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="images/products",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Активность поста"),
                ),
                (
                    "date_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Дата и время подачи",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пост",
                "verbose_name_plural": "Посты",
                "ordering": ("-is_active", "title"),
            },
        ),
        migrations.CreateModel(
            name="PostComments",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "text",
                    models.TextField(default="", verbose_name="Текст комментария"),
                ),
                (
                    "date_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Дата и время создания",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        max_length=200,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        max_length=200,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_app.post",
                        verbose_name="К какому посту",
                    ),
                ),
            ],
            options={
                "verbose_name": "Комментарий к посту",
                "verbose_name_plural": "Комментарии к постам",
                "ordering": ("-date_time", "post"),
            },
        ),
        migrations.CreateModel(
            name="PostRatings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.BooleanField(default=False)),
                ("count", models.PositiveIntegerField(default=0)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_app.post",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рейтинг к новости",
                "verbose_name_plural": "Рейтинги к новостям",
                "ordering": ("-post", "author"),
            },
        ),
        migrations.CreateModel(
            name="Resume",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("iin", models.BigIntegerField()),
                ("text", models.TextField()),
                (
                    "photo",
                    models.ImageField(
                        upload_to="hr/requests/photos", verbose_name="Изображение"
                    ),
                ),
                (
                    "documents",
                    models.FileField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="hr/requests/documents",
                        verbose_name="docs",
                    ),
                ),
                (
                    "date_time",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Дата и время создания",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        help_text='<small class="text-muted">Тут лежит "ссылка" на модель пользователя</small><hr><br>',
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="worker",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Модель пользователя",
                    ),
                ),
            ],
            options={
                "verbose_name": "vakansii",
                "verbose_name_plural": "vakansii",
                "ordering": ("-date_time", "title"),
            },
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "chat_slug",
                    models.ForeignKey(
                        default="changetheslug",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="auth.userprofile",
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("date_added", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        default="default",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="django_app.room",
                    ),
                ),
            ],
            options={
                "ordering": ("-date_added",),
            },
        ),
        migrations.CreateModel(
            name="VacancyRequests",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "resume",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resume",
                        to="django_app.resume",
                    ),
                ),
                (
                    "title",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        help_text='<small class="text-muted">Тут лежит "ссылка" на модель пользователя</small><hr><br>',
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_app.vacancies",
                        verbose_name="Модель ",
                    ),
                ),
            ],
            options={
                "verbose_name": "вакансииzayavki",
                "verbose_name_plural": "вакансииzayavki",
                "ordering": ("-title", "resume"),
            },
        ),
    ]