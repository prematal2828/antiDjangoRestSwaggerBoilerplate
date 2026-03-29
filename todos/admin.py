from django.contrib import admin

from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "priority", "is_completed", "due_date", "created_at")
    list_filter = ("priority", "is_completed")
    search_fields = ("title", "description", "owner__email")
    ordering = ("-created_at",)
    autocomplete_fields = ("owner",)
