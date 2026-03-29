"""
Todo model.
"""

from django.conf import settings
from django.db import models


class Priority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"


class Todo(models.Model):
    """A single todo item belonging to a user."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="todos",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to="todos/images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Todo"
        verbose_name_plural = "Todos"

    def __str__(self) -> str:
        status = "✓" if self.is_completed else "○"
        return f"[{status}] {self.title}"
