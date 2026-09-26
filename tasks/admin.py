from django.contrib import admin

from tasks.models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "status",
        "priority",
        "due_date",
        "created_at",
    )
    
    list_filter = (
        "status",
        "priority",
        "due_date",
    )
    ordering = ("-created_at",)