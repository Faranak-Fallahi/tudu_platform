
from django.conf import settings
from django.db import models


class GoalCategory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="goal_categories",
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "title"],
                name="unique_goal_category_per_user",
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Goal(models.Model):
    class Period(models.TextChoices):
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"
        YEARLY = "yearly", "Yearly"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="goals",
    )
    category = models.ForeignKey(
        GoalCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="goals",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    period = models.CharField(
        max_length=10,
        choices=Period.choices,
    )
    start_date = models.DateField(null=True, blank=True)
    target_date = models.DateField(null=True, blank=True)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        null=True,
        blank=True,
    )
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
