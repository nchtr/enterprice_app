from django.contrib import admin

# Register your models here.

from django_app import models

admin.site.site_header = "Панель управления"  # default: "Django Administration"
admin.site.index_title = "Администрирование сайта"  # default: "Site administration"
admin.site.site_title = "Администрирование"  # default: "Django site admin"


class UserProfileAdmin(admin.ModelAdmin):
    """
    Настройки отображения, фильтрации и поиска модели:'UserProfile' на панели администратора
    """

    list_display = ("user", "avatar", "chat_slug")
    list_display_links = ("user",)
    list_editable = ()
    list_filter = ("user", "avatar", "chat_slug")
    fieldsets = (
        (
            "Основное",
            {"fields": ("user", "avatar")},
        ),
        (
            "Техническое",
            {"fields": ("chat_slug",)},
        ),
    )
    search_fields = ["user", "avatar", "chat_slug"]


admin.site.register(models.UserProfile, UserProfileAdmin)


class PostAdmin(admin.ModelAdmin):
    """
    Настройки отображения, фильтрации и поиска модели:'Post' на панели администратора
    """

    list_display = ("author", "title", "description", "image", "is_active", "date_time")
    list_display_links = (
        "author",
        "title",
        "description",
    )
    list_editable = ("is_active",)
    list_filter = ("author", "title", "description", "image", "is_active", "date_time")
    fieldsets = (
        (
            "Основное",
            {"fields": ("author", "title", "description", "image")},
        ),
        (
            "Техническое",
            {"fields": ("is_active", "date_time")},
        ),
    )
    search_fields = ["title", "description"]


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.PostComments)
admin.site.register(models.PostRatings)


class MessagesAdmin(admin.ModelAdmin):
    """
    Настройки отображения, фильтрации и поиска модели:'Post' на панели администратора
    """

    list_display = (
        "message_id",
        "from_user",
        "to_user",
        "text",
        "is_read",
        "date_time",
    )
    list_display_links = (
        "message_id",
        "from_user",
        "to_user",
        "text",
    )
    list_editable = ("is_read",)
    list_filter = ("message_id", "from_user", "to_user", "text", "is_read", "date_time")
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "from_user",
                    "to_user",
                    "text",
                )
            },
        ),
        (
            "Техническое",
            {"fields": ("is_read", "date_time")},
        ),
    )
    search_fields = ["message_id", "is_read"]


admin.site.register(models.Messages)


class VacanciesAdmin(admin.ModelAdmin):
    """
    Настройки отображения, фильтрации и поиска модели:'Post' на панели администратора
    """

    list_display = (
        "id",
        "title",
        "description",
        "company",
        "image",
        "date_time",
        "is_active",
        "is_distant",
        "salary",
    )
    list_display_links = (
        "title",
        "company",
        "is_active",
        "salary",
    )
    list_editable = ("is_active", "is_distant")
    list_filter = (
        "title",
        "company",
        "date_time",
        "salary",
    )
    fieldsets = (
        (
            "Основное",
            {"fields": ("title", "company", "salary", "is_distant")},
        ),
        (
            "Техническое",
            {"fields": ("is_active", "date_time")},
        ),
    )
    search_fields = ["message_id", "is_read"]


admin.site.register(models.Vacancies)
admin.site.register(models.Resume)
admin.site.register(models.VacancyRequests)


admin.site.register(models.Room)
admin.site.register(models.Message)
