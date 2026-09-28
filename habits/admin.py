from django.contrib import admin
from habits.models import Habit, HabitLog

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "frequency",
        "start_date",
        "end_date",
        "is_active",
        "created_at",
        
    )
    
    list_filter = (
        "frequency",
        "is_active",
        "start_date",
        "end_date",
    )
    
    search_fields = (
        "title",
        "description",
        "user__username",
    )
    
    ordering = ("-created_at",)
    
    
@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = (
        "habit",
        "date",
        "completed",
        "created_at",
    )

    list_filter = (
        "completed",
        "date",
    )

    search_fields = (
        "habit__title",
        "habit__user__username",
    )

    ordering = ("-date",)