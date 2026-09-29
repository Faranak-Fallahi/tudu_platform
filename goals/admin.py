from django.contrib import admin

from goals.models import Goal, GoalCategory

@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display =[
        "title",
        "description",
        "user__email",
        "user__username",
        
    ]
    search_fields = (
        "title",
        "description",
        "user__email",
        "user__username",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
   
@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "category",
        "period",
        "priority",
        "is_completed",
        "start_date",
        "target_date",
        "created_at",
    )
    list_filter = (
        "period",
        "priority",
        "is_completed",
        "created_at",
    )
    search_fields = (
        "title",
        "description",
        "user__email",
        "user__username",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
