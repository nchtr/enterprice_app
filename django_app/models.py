import random
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, pre_delete
from django.utils.timezone import now
from django.utils.text import slugify
from transliterate import translit

# Create your models here.


class UserProfile(models.Model):
    """
    Модель, которая содержит расширение для стандартной модели пользователя веб-платформы
    """

    user = models.OneToOneField(
        editable=True,
        blank=True,
        null=True,
        default=None,
        verbose_name="Модель пользователя",
        help_text='<small class="text-muted">Тут лежит "ссылка" на модель пользователя</small><hr><br>',
        to=User,
        on_delete=models.CASCADE,
        related_name="profile",  # user.profile
    )
    avatar = models.ImageField(
        verbose_name="Аватарка",
        upload_to="users/avatars",
        default=None,
        null=True,
        blank=True,
    )
    chat_slug = models.SlugField(
        default=f"{''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(8))}",
        null=True,
    )

    class Meta:
        """Вспомогательный класс"""

        app_label = "auth"
        ordering = ("-user", "avatar")
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"<UserProfile {self.user.username}>"


@receiver(post_save, sender=User)
def create_user_model(sender, instance, created, **kwargs):
    UserProfile.objects.get_or_create(user=instance)


class Post(models.Model):
    """Наша модель поста"""

    author = models.ForeignKey(
        verbose_name="Автор", to=User, on_delete=models.SET_NULL, null=True, blank=True
    )
    title = models.CharField(max_length=300, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="images/products",
        default=None,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(verbose_name="Активность поста", default=True)
    date_time = models.DateTimeField(default=now, verbose_name="Дата и время подачи")

    class Meta:
        """Вспомогательный класс"""

        app_label = "django_app"
        ordering = ("-is_active", "title")
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return f"<Post {self.title} {self.author.username}>"


class PostComments(models.Model):
    """Комментарии к постам"""

    post = models.ForeignKey(
        to=Post, verbose_name="К какому посту", max_length=200, on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        to=User, verbose_name="Автор", max_length=200, on_delete=models.CASCADE
    )  # +-
    text = models.TextField("Текст комментария", default="")
    date_time = models.DateTimeField("Дата и время создания", default=now)

    class Meta:
        app_label = "django_app"
        ordering = ("-date_time", "post")
        verbose_name = "Комментарий к посту"
        verbose_name_plural = "Комментарии к постам"

    def __str__(self):
        return f"{self.date_time} {self.author.username} {self.post.title} {self.text[:20]}"


class PostRatings(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)  # OneToMany +-
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    count = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = "django_app"
        ordering = ("-post", "author")
        verbose_name = "Рейтинг к новости"
        verbose_name_plural = "Рейтинги к новостям"

    def __str__(self):
        if self.status and self.count >= 9999:
            like = "ЛАЙК"
            count = "9999+"
        else:
            like = "ДИЗЛАЙК"
            count = str(self.count)

        return f"{self.post.title} {self.author.username} {count} {like}"


class Vacancies(models.Model):
    title = models.CharField(max_length=250, verbose_name="naming")
    description = models.TextField(verbose_name="desc")
    company = models.CharField(max_length=100)
    date_time = models.DateTimeField("Дата и время создания", default=now)
    is_active = models.BooleanField(verbose_name="activity", default=False)
    is_distant = models.BooleanField(verbose_name="worktype", default=False)
    salary = models.IntegerField()
    slug = models.SlugField(default="changeit")

    class Meta:
        app_label = "django_app"
        ordering = ("-date_time", "title")
        verbose_name = "вакансии"
        verbose_name_plural = "вакансии"

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(f"{self.title}", "ru", reversed=True)+"-"+translit(f"{self.company}", "ru", reversed=True))
        super(Vacancies, self).save(*args, **kwargs)

    def __str__(self):
        return f"<Vacancy {self.title} {self.description} {self.company} {self.salary} {self.date_time} {self.is_active} {self.is_distant} {self.slug}>"


class Resume(models.Model):
    person = models.ForeignKey(
        blank=True,
        null=True,
        default=None,
        verbose_name="Модель пользователя",
        help_text='<small class="text-muted">Тут лежит "ссылка" на модель пользователя</small><hr><br>',
        to=User,
        on_delete=models.CASCADE,
        related_name="worker",  # user.profile
    )
    title = models.CharField(max_length=150)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    iin = models.BigIntegerField()
    text = models.TextField()
    photo = models.ImageField(
        verbose_name="Изображение", upload_to="hr/requests/photos"
    )
    documents = models.FileField(
        verbose_name="docs",
        upload_to="hr/requests/documents",
        default=None,
        null=True,
        blank=True,
    )
    date_time = models.DateTimeField("Дата и время создания", default=now)

    class Meta:
        app_label = "django_app"
        ordering = ("-date_time", "title")
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"

    def __str__(self):
        return f"<Resume {self.person.username} {self.title} {self.first_name} {self.last_name} {self.iin} {self.text} {self.photo} {self.documents} {self.date_time}>"


class VacancyRequests(models.Model):
    title = models.ForeignKey(
        to=Vacancies,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
        verbose_name="Модель ",
        help_text='<small class="text-muted">Тут лежит "ссылка" на модель пользователя</small><hr><br>',
    )
    resume = models.ForeignKey(
        to=Resume, related_name="resume", on_delete=models.CASCADE
    )

    class Meta:
        app_label = "django_app"
        ordering = ("-title", "resume")
        verbose_name = "Отклики на вакансии"
        verbose_name_plural = "Отклики на вакансии"

    def __str__(self):
        return f"<VacRequest {self.title.title} {self.resume.title}>"


class Messages(models.Model):
    message_id = models.BigAutoField(
        primary_key=True,
        unique=True,
        verbose_name="айди сообщения",
        null=False,
        blank=False,
        auto_created=True,
    )
    from_user = models.OneToOneField(
        to=User, default="Аноним", on_delete=models.CASCADE, related_name="sender"
    )
    to_user = models.OneToOneField(
        to=User, default="Админ_нейм", on_delete=models.CASCADE, related_name="reciever"
    )
    text = models.TextField(default="Пустое сообщение.")
    date_time = models.DateTimeField("Дата и время создания", default=now)
    is_read = models.BooleanField(default=False)

    class Meta:
        app_label = "django_app"
        ordering = ("-message_id", "-date_time")
        verbose_name = "Голубиная почта"
        verbose_name_plural = "Почта"

    def __str__(self):
        return f"<Message {self.message_id} {self.text} {self.from_user.username} {self.to_user.username} {self.date_time} {self.is_read}>"


class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.ForeignKey(
        to=UserProfile, on_delete=models.CASCADE, default="changetheslug"
    )

    class Meta:
        app_label = "django_app"
        ordering = ("name",)
        verbose_name = "Комнаты"
        verbose_name_plural = "Комнаты"

    def __str__(self):
        return f"<Room {self.name} {self.slug.chat_slug}>"


class Message(models.Model):
    room = models.ForeignKey(
        Room, related_name="messages", on_delete=models.CASCADE, default="default"
    )
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "django_app"
        ordering = ("-date_added",)
        verbose_name = "Сообщения"
        verbose_name_plural = "Сообщения"
