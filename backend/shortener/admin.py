from django.contrib import admin
from .models import Link, Click


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "short_code",
        "original_url",
        "click_count",
        "created_at",
    )

    search_fields = (
        "short_code",
        "original_url",
    )

    readonly_fields = ("created_at",)

    def click_count(self, obj):
        return obj.clicks.count()

    click_count.short_description = "Clicks"


@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "link",
        "ip_address",
        "created_at",
    )

    search_fields = (
        "link__short_code",
        "ip_address",
    )

    readonly_fields = ("created_at",)
