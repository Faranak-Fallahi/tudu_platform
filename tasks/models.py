from django.db import models

from config import settings

class Task(models.Model):
    STATUS_CHOICES = [
    ("TODO", "To Do"),
    ("IN_PROGRESS", "In Progress"),
    ("COMPLETED", "Completed"),
    ]
    
    PRIORITY_CHOICES = [
    ("LOW", "Low"),
    ("MEDIUM", "Medium"),
    ("HIGH", "High"),
    ("URGENT", "Urgent"),
    ]   
    
    user = models.ForeignKey(
        
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
        
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default="TODO",
    )
    
    priority = models.CharField(
    max_length=10,
    choices=PRIORITY_CHOICES,
    default="MEDIUM",
    )
    
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=["user", "due_date"]),
        ]