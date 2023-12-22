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

    list_display = ("user", "avatar")
    list_display_links = ("user",)
    list_editable = ()
    list_filter = ("user", "avatar")
    fieldsets = (
        (
            "Основное",
            {"fields": ("user", "avatar")},
        ),
        (
            "Техническое",
            {"fields": ()},
        ),
    )
    search_fields = ["user", "avatar"]


admin.site.register(models.UserProfile, UserProfileAdmin)