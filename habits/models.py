from django.conf import settings
from django.db import models


class Habit(models.Model):
    class Frequency(models.TextChoices):
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    start_date = models.DateField()

    end_date = models.DateField()

    frequency = models.CharField(
        max_length=20,
        choices=Frequency.choices,
        default=Frequency.DAILY,
    )

    target_count = models.PositiveIntegerField(
        default=1,
    )

    target_days = models.JSONField(
        default=list,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class HabitLog(models.Model):
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="logs",
    )

    date = models.DateField()

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

        constraints = [
            models.UniqueConstraint(
                fields=["habit", "date"],
                name="unique_habit_log_per_day",
            )
        ]

    def __str__(self):
        return f"{self.habit.title} - {self.date}"