from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, pre_delete
from django.utils.timezone import now

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
    avatar = models.ImageField(verbose_name="Аватарка", upload_to="users/avatars", default=None, null=True, blank=True)

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

    author = models.ForeignKey(verbose_name="Автор", to=User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=300, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(verbose_name="Изображение", upload_to="images/products", default=None, null=True, blank=True)
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

    post = models.ForeignKey(to=Post, verbose_name="К какому посту", max_length=200, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, verbose_name="Автор", max_length=200, on_delete=models.CASCADE)  # +-
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
        if self.status and self.count>=9999:
            like = "ЛАЙК"
            count = "9999+"
        else:
            like = "ДИЗЛАЙК"
            count = str(self.count)
            
        return f"{self.post.title} {self.author.username} {count} {like}"
    
    
class Vacancies(models.Model):
    title=models.CharField(max_length=250, verbose_name='naming')
    desciption=models.TextField(verbose_name="desc")
    company=models.CharField(max_length=100)
    image=models.ImageField(verbose_name="Изображение", upload_to="hr/vacancies", default=None, null=True, blank=True)
    date_time=models.DateTimeField("Дата и время создания", default=now)
    is_active=models.BooleanField(verbose_name='activity', default=False)
    is_distant=models.BooleanField(verbose_name='worktype', default=False)
    salary=models.IntegerField(max_length=10)
    class Meta:
        app_label = "django_app"
        ordering = ("-date_time")
        verbose_name = "вакансии"
        verbose_name_plural = "вакансии"
    def __str__(self):
        return f"<Vacancy {self.title} {self.desciption} {self.company} {self.image} {self.salary} {self.date_time} {self.is_active} {self.is_distant}>"

class Resume(models.Model):
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
    title=models.CharField(max_length=150)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    iin=models.BigIntegerField(max_length=12)
    text=models.TextField()
    photo=models.ImageField(verbose_name="Изображение", upload_to="hr/requests/photos")
    documents=models.FileField(verbose_name="docs", upload_to="hr/requests/documents", default=None, null=True, blank=True)
    date_time=models.DateTimeField("Дата и время создания", default=now)
    
    class Meta:
        app_label = "django_app"
        ordering = ("-date_time")
        verbose_name = "vakansii"
        verbose_name_plural = "vakansii"
    def __str__(self):
         return f"<Resume {self.user.username} {self.title} {self.first_name} {self.last_name} {self.iin} {self.text} {self.photo} {self.documents} {self.date_time}>"

class VacancyRequests(models.Model):
    title=models.ForeignKey(to=Vacancies, on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
        verbose_name="Модель ",
        help_text='<small class="text-muted">Тут лежит "ссылка" на модель пользователя</small><hr><br>')
    resume = models.ForeignKey(to=Resume, related_name='resume', on_delete=models.CASCADE)
    class Meta:
        app_label = "django_app"
        ordering = ("-title")
        verbose_name = "вакансииzayavki"
        verbose_name_plural = "вакансииzayavki"

    def __str__(self):
        return f'<VacRequest {self.title.title} {self.resume.title}>'
    