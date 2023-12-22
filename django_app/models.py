from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, pre_delete

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
    
    
    
# class Posts(models.Model):
#     id = models.IntegerField(primary_key=True, auto_created=True)
#     title = models.TextField()
#     author = models.TextField()
#     desc = models.TextField()
#     media = models.FileField()
#     approved = models.BooleanField()
    
#     class Meta:
#         app_label = "posts"
#         ordering = ("-id", "author")
#         verbose_name = "posti"
#         verbose_name_plural = "posti"

#     def __str__(self):
#         return f"{self.id}, {self.title}, {self.author}, {self.desc}, {self.approved}"