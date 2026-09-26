from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Case, When, IntegerField

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        date = self.request.query_params.get("date")

        if date:
            queryset = queryset.filter(due_date=date)
        else:
            queryset = queryset.filter(due_date=timezone.localdate())

        priority_order = Case(
            When(priority="URGENT", then=1),
            When(priority="HIGH", then=2),
            When(priority="MEDIUM", then=3),
            When(priority="LOW", then=4),
            output_field=IntegerField(),
        )

        return queryset.order_by(
            priority_order,
            "created_at",
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
class TaskUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)